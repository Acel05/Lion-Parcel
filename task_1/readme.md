# Lion Parcel Data Engineer Test

## Task 1: ETL Retail Transactions
- **Tool**: Apache Airflow & PostgreSQL.
- **Sync Method**: Incremental Upsert via `updated_at`.
- **Soft Delete**: Data di warehouse tetap ada dengan kolom `deleted_at` yang terupdate untuk keperluan audit.

## How to Run
1. `cd task_1`
2. `docker compose up -d`
3. Access Airflow at `http://localhost:8080` (admin/admin).