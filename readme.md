# Lion Parcel Technical Test - Data Engineer

Repositori ini berisi solusi untuk Tes Teknis Lion Parcel yang mencakup otomatisasi workflow (Airflow) dan pengembangan API (FastAPI + AI).

---

## Task 1: Airflow Workflow Automation
**Deskripsi**: Sinkronisasi data transaksi retail dari skema `source` ke `warehouse` dengan metode Incremental Load dan penanganan Soft Delete.

### Cara Menjalankan:
1. Masuk ke folder `task_1`.
2. Jalankan `docker-compose up -d` di terminal.
3. Akses Airflow UI di `http://localhost:8080` (admin/admin).
4. Buat koneksi `postgres_default` di menu Admin -> Connections.
5. Aktifkan DAG `lion_parcel_etl_v1`.

---

## Task 2: Image API & Batch Processing
**Deskripsi**: API untuk mendeteksi keburaman gambar (OpenCV) dan mendeskripsikan konten gambar menggunakan Gemini AI (Substitusi OpenAI).

### Fitur:
- **POST /predict**: Menerima URL gambar (internet/Google Drive).
- **GET /process_local_dataset**: Merangkum dataset lokal ke dalam file CSV dengan deskripsi AI asli.
- **GET /process_drive_folder/{id}**: Mengotomatisasi pemrosesan seluruh folder Google Drive ke CSV.

### Cara Menjalankan:
1. Masuk ke folder `task_2_api`.
2. Pastikan file `.env` berisi `GEMINI_API_KEY`.
3. Jalankan container dengan volume mounting:
   ```bash
   docker run -p 8000:8000 \
     -v "${PWD}/images:/app/images" \
     -v "${PWD}:/app/data" \
     --env-file .env \
     lion-parcel-api