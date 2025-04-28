from fastapi import FastAPI
from backend.api.v1 import image_api, invoice_api
from backend.core.config import settings

app = FastAPI()

# 注册 API 路由
app.include_router(image_api.router, prefix="/api/v1/invoice")
app.include_router(invoice_api.router, prefix="/api/v1/download")