import logging
import os
from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import FileResponse
import fitz  # PyMuPDF
import requests
import openpyxl
from pathlib import Path
from backend.utils import perform_ocr, save_excel, extract_invoice_data
import re

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

# 批量上传并处理发票
@app.post("/process_invoices/")
async def process_invoices(files: list[UploadFile], language: str = Form("chi_sim")):
    output_dir = Path("backend/static/")
    output_dir.mkdir(parents=True, exist_ok=True)  # 确保路径存在
    
    # 批量保存 PDF 到临时文件夹并从PDF提取图像
    extracted_data = []
    for file in files:
        pdf_path = output_dir / file.filename
        with pdf_path.open("wb") as f:
            f.write(await file.read())  # 异步读取文件内容

        # 转换 PDF 页到图像
        pdf_document = fitz.open(pdf_path)
        for page_number in range(len(pdf_document)):
            page = pdf_document[page_number]

            # 渲染 PDF 页面为像素图像
            mat = fitz.Matrix(2,2)  # 放大倍数
            pix = page.get_pixmap(matrix=mat)
            # pix = page.get_pixmap(dpi=100)  

            # 保存页面图像为临时文件
            temp_image_path = output_dir / f"{file.filename}_page_{page_number + 1}.png"
            pix.save(temp_image_path)


            

            # OCR API 调用并解析结果
            ocr_result = perform_ocr(temp_image_path, language)
            ocr_result=extract_invoice_data(ocr_result)

            # print(f"OCR 结果: {ocr_result}")
            logging.info(f"OCR 结果: {ocr_result}")
            extracted_data.append({
                "file": file.filename,
                "page": page_number + 1,
                "text": ocr_result # 这里可以根据需要调整提取的字段
            })

            # 删除临时图像文件
            temp_image_path.unlink()

        # 关闭 PDF 文件
        pdf_document.close()

        # 删除临时 PDF 文件
        pdf_path.unlink()

    # 保存数据到 Excel 并提供下载链接
    excel_file_path = output_dir / "extracted_data.xlsx"
    # save_excel(extracted_data, str(excel_file_path))
    body = {
        "message": "success",
        "code": 200,
        "status": 200,
        "data":{
            "extracted_data": extracted_data,
            "excel_file_path": str(excel_file_path)
        },
        
    }

    return body
            

# 提供Excel下载
@app.get("/download/{file_name}")
async def download_file(file_name: str):
    file_path = Path("backend/static/") / file_name
    if file_path.exists():
        return FileResponse(path=str(file_path), filename=file_name, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    return {"error": "File not found"}