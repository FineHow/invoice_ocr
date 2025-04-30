import os
from fastapi import FastAPI, UploadFile, Form
import fitz  # PyMuPDF
import requests
import openpyxl
import aiofiles
import uuid
from pathlib import Path
from backend.core.utils  import  umi_ocr,umi_invoice_data
from backend.core.ziprar import handle_zip_uploaded
from backend.core.download import save_excel
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import numpy as np
from dotenv import load_dotenv
from backend.core.config import settings

# 加载环境变量
# load_dotenv()
# OCR_API_BASE_URL = os.getenv("OCR_API_BASE_URL")

app = FastAPI()
# 批量上传并处理发票

from fastapi import APIRouter
router = APIRouter()
@router.post("/normalocr/", tags=["OCR识别"])
async def process_invoices2(files: list[UploadFile], language: str = Form("chi_sim")):
    output_dir = Path("backend/static/")
    output_dir.mkdir(parents=True, exist_ok=True)  # 确保路径存在
    # 批量保存 PDF 到临时文件夹并从PDF提取图像
    extracted_data = []
    # 处理 ZIP 文件
    for file in files:
        if file.filename.endswith('.zip'):
            # 保存 ZIP 文件到指定目录
            unique_filename = f"{uuid.uuid4()}_{file.filename}"  # uuid确保文件名唯一,防止多个用户使用相同字段
            zip_path = output_dir / unique_filename
            async with aiofiles.open(zip_path, mode="wb") as f:
                await f.write(await file.read())
            # 调用解压函数
            handle_zip_uploaded(zip_path, output_dir)   
            # 遍历解压后的文件夹，找到所有 PDF 文件
            extracted_files = [
                p for p in output_dir.iterdir() if p.suffix == '.pdf'
            ]
            for pdf_file in extracted_files:
                # PDF 文件后续处理逻辑（转换 PDF 页面到图像等）
                pdf_path = pdf_file  # pdf_file 是解压后的 PDF 文件路径
                pdf_document = fitz.open(pdf_path)
                
                for page_number in range(len(pdf_document)):
                    page = pdf_document[page_number]
                    mat = fitz.Matrix(5, 5)
                    pix = page.get_pixmap(matrix=mat)

                    # 保存页面图像为临时文件
                    temp_image_path = output_dir / f"{pdf_file.stem}_page_{page_number + 1}.png"
                    pix.save(temp_image_path)
                    # 调用 OCR 处理图像
                    ocr_result = umi_ocr(temp_image_path)

                    extracted_data.append({
                        "file": pdf_file.name,
                        "page": page_number + 1,
                        "text": str(ocr_result)
                    })

                    # 删除临时图像文件
                    temp_image_path.unlink()

                pdf_document.close()
                # 删除 PDF 
                pdf_path.unlink()

        elif file.filename.endswith('.pdf'):
            # 如果单独发送批量 PDF 文件
            pdf_path = output_dir / file.filename
            async with aiofiles.open(pdf_path, mode="wb") as f:
                await f.write(await file.read())

            pdf_document = fitz.open(pdf_path)
            for page_number in range(len(pdf_document)):
                page = pdf_document[page_number]
                mat = fitz.Matrix(5, 5)
                pix = page.get_pixmap(matrix=mat)

                temp_image_path = output_dir / f"{file.filename}_page_{page_number + 1}.png"
                pix.save(temp_image_path)

                ocr_result = umi_ocr(temp_image_path)

                extracted_data.append({
                    "file": file.filename,
                    "page": page_number + 1,
                    "text": str(ocr_result)
                })

                temp_image_path.unlink()

            pdf_document.close()
            pdf_path.unlink()

        else:
            return {"error": "文件格式错误，请上传 PDF 文件或 ZIP 文件！"}
    
    # 保存 Excel 文件   
    # excel_file_path = output_dir / "extracted_data.xlsx"
    # save_excel(extracted_data, excel_file_path)

    body = {
        "message": "success",
        "code": 200,
        "status": 200,
        "data": {
            "extracted_data": extracted_data,
            # "excel_file_path": str(excel_file_path),
            "download_link": f"{settings.APP_HOST}:{settings.APP_PORT}/api/v1/download/download/extracted_data.xlsx",
            },
        }
        

    return body