from fastapi import FastAPI
from backend.api.v1 import  invoice,download
from backend.core.config import settings


import requests
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# 加载环境变量
# settings = settings()
load_dotenv()
OCR_API_BASE_URL = os.getenv("OCR_API_BASE_URL")


app = FastAPI()


# 注册 API 路由
app.include_router(invoice.router, prefix="/api/v1/invoice")
app.include_router(download.router,prefix="/api/v1/download")


# health检查
@app.get("/")
async def health_check():
    try:
        response = requests.get(OCR_API_BASE_URL + "/")
        return {"message": response.json()}
    except Exception as e:
        return {"error": str(e)}