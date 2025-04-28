from fastapi import FastAPI
from backend.api.v1 import  invoice,download
from backend.core.config import settings
import requests
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()


# 注册 API 路由
app.include_router(invoice.router, prefix="/api/v1/invoice")
app.include_router(download.router,prefix="/api/v1/download")


# health检查tessart
@app.get("/tessart",tags=["ocr服务检查"])
async def health_check():
    try:
        response = requests.get(settings.OCR_API_BASE_URL + "/")
        return {"message": response.json()}
    except Exception as e:
        return {"error": str(e)}

# health检查umiocr
@app.get("/umiocr",tags=["ocr服务检查"])
async def health_check():
    try:
        response = requests.get(settings.UMIOCR_API_BASE_URL + "/")
        return {"message": response.json()}
    except Exception as e:
        return {"error": str(e)}