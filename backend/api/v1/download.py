import logging
import os
from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import FileResponse
import fitz  # PyMuPDF
import requests



from pathlib import Path
from backend.utils  import perform_ocr, save_excel, extract_invoice_data, umi_ocr,umi_invoice_data
from backend.modelpro import extract_invoice_data_with_gemma,test_gemma_chat
from backend.download import save_excel
from backend.ziprar import handle_zip_uploaded
from fastapi.middleware.cors import CORSMiddleware

from PIL import Image
import numpy as np
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()
OCR_API_BASE_URL = os.getenv("OCR_API_BASE_URL")

app = FastAPI()

# health检查
@app.get("/")
async def health_check():
    try:
        response = requests.get(OCR_API_BASE_URL + "/")
        return {"message": response.json()}
    except Exception as e:
        return {"error": str(e)}


            
# 提供Excel下载
@app.get("/download/{file_name}")
async def download_file(file_name: str):
    file_path = Path("backend/static/") / file_name
    if file_path.exists():
        return FileResponse(path=str(file_path), filename=file_name, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    return {"error": "File not found"}