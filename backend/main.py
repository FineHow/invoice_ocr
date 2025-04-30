from fastapi import FastAPI
from backend.api.v1 import  invoice,download,normalocr
from backend.core.config import settings
import requests
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()



# 配置 CORS
origins = [
    f"{settings.APP_HOST}:{settings.APP_PORT}",  # 本地开发地址
    "http://localhost:5173",  # 前端开发地址
    "http://127.0.0.1:3000",  # 前端开发地址
    # "http://your-frontend-domain.com",  # 部署的前端域名
]

app.add_middleware(
    CORSMiddleware,
    # allow_origins=["http://localhost:5173"],  # 如果允许特定源
    allow_origins=origins,  # 允许的源
    allow_credentials=True,  # 允许跨域携带 Cookie
    allow_methods=["*"],  # 允许的方法
    allow_headers=["*"],  # 允许的请求头
)

# 注册 API 路由
app.include_router(invoice.router, prefix="/api/v1/invoice")
app.include_router(download.router,prefix="/api/v1/download")
app.include_router(normalocr.router,prefix="/api/v1/normalocr")


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