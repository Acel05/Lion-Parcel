FROM python:3.10-slim

# Install library sistem dasar yang dibutuhkan oleh OpenCV
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install dependensi Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Salin script dan dataset
COPY . .

# Port standar untuk FastAPI
EXPOSE 8000

# Menjalankan server aplikasi
CMD ["uvicorn", "app:app", "--host", "localhost", "--port", "8000"]