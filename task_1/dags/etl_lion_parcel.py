from airflow import DAG
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'lion_parcel',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
}

def sync_retail_data():
    """
    Mengambil data dari schema 'source' dan melakukan UPSERT 
    ke schema 'warehouse' untuk sinkronisasi data transaksi.
    """
    pg_hook = PostgresHook(postgres_conn_id='postgres_default')
    
    # EXTRACT: Ambil data yang berubah dalam 1 jam terakhir
    extract_query = """
        SELECT id, customer_id, last_status, pos_origin, pos_destination, created_at, updated_at, deleted_at 
        FROM source.retail_transactions 
        WHERE updated_at >= NOW() - INTERVAL '24 hours';;
    """
    records = pg_hook.get_records(extract_query)

    if records:
        for row in records:
            # LOAD & SYNC: Update jika ID sudah ada (Handle Updates & Soft Deletes)
            upsert_query = """
                INSERT INTO warehouse.retail_transactions 
                (id, customer_id, last_status, pos_origin, pos_destination, created_at, updated_at, deleted_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO UPDATE SET
                    last_status = EXCLUDED.last_status,
                    updated_at = EXCLUDED.updated_at,
                    deleted_at = EXCLUDED.deleted_at;
            """
            pg_hook.run(upsert_query, parameters=row)

with DAG(
    'lion_parcel_etl_v1',
    default_args=default_args,
    description='Sinkronisasi Incremental Retail Transactions',
    schedule_interval='@hourly',
    catchup=False
) as dag:

    task_sync = PythonOperator(
        task_id='sync_source_to_warehouse',
        python_callable=sync_retail_data
    )