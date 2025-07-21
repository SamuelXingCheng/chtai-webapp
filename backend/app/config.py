import os
from dotenv import load_dotenv

# 自動載入 .env
load_dotenv()

class Settings:
    ENV: str = os.getenv("ENV", "development")
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "CHTAI WebApp")
    FIREBASE_CREDENTIALS_PATH: str = os.getenv("FIREBASE_CREDENTIALS_PATH", "./serviceAccountKey.json")

settings = Settings()
