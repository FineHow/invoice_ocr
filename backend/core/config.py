import os
from dotenv import load_dotenv

class Settings:
    def __init__(self):
        env = os.getenv("APP_ENV", "development")
        if env == "production":
            load_dotenv(".env.production")
        else:
            load_dotenv(".env.development")

        self.APP_HOST = os.getenv("APP_HOST")
        self.APP_PORT = int(os.getenv("APP_PORT", 8000))
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")
        self.RELOAD = os.getenv("RELOAD", "True") == "True"
        self.DATABASE_URI = os.getenv("DATABASE_URI")

settings = Settings()