# Lion Parcel Technical Test - Data Engineer

Repositori ini berisi solusi lengkap untuk Tes Teknis Lion Parcel, mencakup otomatisasi workflow data (Airflow) dan pengembangan API analisis gambar berbasis AI (FastAPI + Gemini).

---

## Task 1: Airflow Workflow Automation
**Deskripsi**: Pipeline ETL untuk sinkronisasi data transaksi retail dari skema `source` ke `warehouse` menggunakan metode Incremental Load (filter 24 jam) dan penanganan Soft Delete.

### Cara Menjalankan:
1. Masuk ke folder `task_1`.
2. Jalankan docker-compose di terminal: 
       ```bash
       docker-compose up -d 
3. Akses Airflow UI di `http://localhost:8080` (User: admin | Pass: admin).
4. Konfigurasi Koneksi:
- Buka menu Admin -> Connections.
- Tambah koneksi baru:
    - **Conn Id**: postgres_default
    - **Conn Type**: Postgres
    - **Host**: postgres
    - **Database**: lionparcel_db
    - **Login**: lionuser
    - **Password**: lionpass
5. Aktifkan DAG `lion_parcel_etl_v1` dan trigger untuk memulai sinkronisasi.

---

## Task 2: Image API & Batch Processing
**Deskripsi**: API untuk mendeteksi keburaman gambar menggunakan varians Laplacian (OpenCV) dan menghasilkan deskripsi konten gambar menggunakan Gemini AI.

### Fitur:
- **POST /predict**: Menerima URL gambar (internet/Google Drive).
- **GET /process_local_dataset**: Batch processing gambar di folder `images/` ke dalam file `data/summary_local.csv`.
- **GET /process_drive_folder/{id}**: Otomatisasi download dan analisis folder Google Drive ke `data/summary_drive.csv`.

### Cara Menjalankan:
1. Masuk ke folder `task_2`.
2. Pastikan file `.env` berisi `GEMINI_API_KEY`.
3. (Opsional) Masukkan service-account.json jika ingin mencoba fitur Google Drive.
4. Build Image:
    ```Bash
    docker build -t lion-parcel-api .
4. Jalankan Container dengan Volume Mounting (untuk persistensi hasil CSV):
   ```bash
   docker run -p 8000:8000 \
     -v "${PWD}/images:/app/images" \
     -v "${PWD}:/app/data" \
     -v "${PWD}/service-account.json:/app/service-account.json" \
     --env-file .env \
     lion-parcel-api

📸 Proof of Work (Screenshots)
Bukti visual eksekusi sistem dapat dilihat pada folder berikut:
- `task_1/screenshots/`: Graph View, Grid History, dan DB Verification.
- `task_2/data/`: Hasil CSV dengan deskripsi AI.