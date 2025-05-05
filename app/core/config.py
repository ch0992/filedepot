"""
app/core/config.py
공통 환경설정 관리 (예: 환경 변수 로딩)
"""

import os

class Settings:
    def __init__(self):
        self.ENV = os.getenv("ENV") or "development_k8s"
        if self.ENV == "development":
            self.FILE_SERVICE_URL = os.getenv("FILE_SERVICE_URL", "http://localhost:8001")
            self.DATA_SERVICE_URL = os.getenv("DATA_SERVICE_URL", "http://localhost:8002")
            self.LOG_SERVICE_URL = os.getenv("LOG_SERVICE_URL", "http://localhost:8003")
        else:  # development_k8s, stage, production 등
            self.FILE_SERVICE_URL = os.getenv("FILE_SERVICE_URL", "http://file:8001")
            self.DATA_SERVICE_URL = os.getenv("DATA_SERVICE_URL", "http://data:8002")
            self.LOG_SERVICE_URL = os.getenv("LOG_SERVICE_URL", "http://log:8003")
        

settings = Settings()
