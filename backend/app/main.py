# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="CHTAI WebApp API",
    version="0.1.0"
)

# CORS 設定：允許前端 Vue3 呼叫
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 健康檢查 API
@app.get("/health")
def health_check():
    return {"status": "ok", "message": "API is running"}