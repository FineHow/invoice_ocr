import logging
import os
from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import FileResponse
import fitz  # PyMuPDF
import requests
from pathlib import Path
from backend.utils  import perform_ocr, save_excel, extract_invoice_data, umi_ocr,umi_invoice_data
from backend.core.modelpro import extract_invoice_data_with_gemma,test_gemma_chat
from backend.core.download import save_excel
from backend.core.ziprar import handle_zip_uploaded
from fastapi.middleware.cors import CORSMiddleware

from PIL import Image
import numpy as np
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()
OCR_API_BASE_URL = os.getenv("OCR_API_BASE_URL")


from fastapi import APIRouter
router = APIRouter()   
# 提供Excel下载
@router.get("/download/{file_name}", tags=["下载处理表格"])
async def download_file(file_name: str):
    file_path = Path("backend/static/") / file_name
    if file_path.exists():
        return FileResponse(path=str(file_path), filename=file_name, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    return {"error": "File not found"}