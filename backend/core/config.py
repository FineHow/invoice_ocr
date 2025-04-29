import os
from dotenv import load_dotenv

# 动态加载 .env 文件
env = os.getenv("APP_ENV", "development")
if env == "production":
    load_dotenv(".env.production")
else:
    load_dotenv(".env.development")

class Settings:
    UMIOCR_API_BASE_URL = os.getenv("UMIOCR_API_BASE_URL")
    OCR_API_BASE_URL = os.getenv("OCR_API_BASE_URL")
    OLLAMA_PROXY_URL = os.getenv("OLLAMA_PROXY_URL")
    APP_HOST = os.getenv("APP_HOST", "127.0.0.1")
    APP_PORT = int(os.getenv("APP_PORT", 8000))
    LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")
    RELOAD = os.getenv("RELOAD", "True") == "True"

# 全局 Settings 实例
settings = Settings()