import cv2
import numpy as np
import os
import csv
import requests
import io
import google.generativeai as genai
from fastapi import FastAPI, HTTPException
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

# Konfigurasi AI (Gemini 2.5 Flash)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-flash')

# Konfigurasi Google Drive API
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
SERVICE_ACCOUNT_FILE = 'service-account.json'

def get_drive_service():
    if os.path.exists(SERVICE_ACCOUNT_FILE):
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        return build('drive', 'v3', credentials=creds)
    return None

def get_image_status(img_bytes):
    """Mendeteksi keburaman menggunakan varians Laplacian."""
    nparr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None: return False
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    variance = cv2.Laplacian(gray, cv2.CV_64F).var()
    return variance < 100.0

# --- OPTION 1: PREDICT VIA URL (Manual) ---
@app.post("/predict")
async def predict_image(payload: dict):
    image_url = payload.get("image_url")
    if not image_url:
        raise HTTPException(status_code=400, detail="image_url is required")
    
    try:
        response = requests.get(image_url, timeout=15)
        image_content = response.content
        
        if get_image_status(image_content):
            return {"result": "blur"}
        
        ai_resp = model.generate_content([
            "Describe the content of this image in text form.",
            {"mime_type": "image/jpeg", "data": image_content}
        ])
        return {"result": ai_resp.text.strip()}
    except Exception as e:
        return {"result": f"Error: {str(e)}"}

# --- OPTION 2: PROCESS LOKAL FOLDER (Otomatis ke CSV) ---
@app.get("/process_local_dataset")
def process_local():
    image_folder = "images"
    output_csv = "data/summary_local.csv"
    results = []
    
    if not os.path.exists(image_folder):
        return {"error": f"Folder {image_folder} tidak ditemukan"}

    for filename in os.listdir(image_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            path = os.path.join(image_folder, filename)
            with open(path, "rb") as f:
                content = f.read()
            
            if get_image_status(content):
                res = "blur"
            else:
                try:
                    # Mendapatkan deskripsi AI asli untuk CSV
                    resp = model.generate_content([
                        "Describe the content of this image in text form.",
                        {"mime_type": "image/jpeg", "data": content}
                    ])
                    res = resp.text.strip()
                except Exception as e:
                    res = f"AI Error: {str(e)}"
            
            results.append([filename, res])
            
    os.makedirs("data", exist_ok=True)
    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["file_name", "result"])
        writer.writerows(results)
    return {"status": "success", "file": output_csv}

# --- OPTION 3: PROCESS DRIVE FOLDER (Otomatis ke CSV) ---
@app.get("/process_drive_folder/{folder_id}")
async def process_drive(folder_id: str):
    service = get_drive_service()
    if not service:
        raise HTTPException(status_code=500, detail="Service account file missing")
    
    results = []
    output_csv = "data/summary_drive.csv"
    
    try:
        query = f"'{folder_id}' in parents and mimeType contains 'image/'"
        files = service.files().list(q=query, fields="files(id, name, mimeType)").execute().get('files', [])
        
        for file in files:
            request = service.files().get_media(fileId=file['id'])
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while not done: _, done = downloader.next_chunk()
            
            img_bytes = fh.getvalue()
            
            if get_image_status(img_bytes):
                res = "blur"
            else:
                try:
                    # Mendapatkan deskripsi AI asli untuk CSV
                    resp = model.generate_content([
                        "Describe the content of this image in text form.",
                        {"mime_type": file['mimeType'], "data": img_bytes}
                    ])
                    res = resp.text.strip()
                except Exception as e:
                    res = f"AI Error: {str(e)}"
            
            results.append([file['name'], res])
            
        os.makedirs("data", exist_ok=True)
        with open(output_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["file_name", "result"])
            writer.writerows(results)
        return {"status": "success", "file": output_csv}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))