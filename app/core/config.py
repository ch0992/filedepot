"""
app/core/config.py
공통 환경설정 관리 (예: 환경 변수 로딩)
"""

import os

class Settings:
    ENV: str = os.getenv("ENV", "development_local")
    if ENV == "development_local":
        FILE_SERVICE_URL = os.getenv("FILE_SERVICE_URL", "http://localhost:8001")
        DATA_SERVICE_URL = os.getenv("DATA_SERVICE_URL", "http://localhost:8002")
        LOG_SERVICE_URL = os.getenv("LOG_SERVICE_URL", "http://localhost:8003")
    else:  # development_k8s, stage, production
        FILE_SERVICE_URL = os.getenv("FILE_SERVICE_URL", "http://file:8001")
        DATA_SERVICE_URL = os.getenv("DATA_SERVICE_URL", "http://data:8002")
        LOG_SERVICE_URL = os.getenv("LOG_SERVICE_URL", "http://log:8003")

settings = Settings()
