"""
app/core/config.py
공통 환경설정 관리 (예: 환경 변수 로딩)
"""

import os

class Settings:
    ENV: str = os.getenv("ENV", "development")
    # 추가 설정 항목

settings = Settings()
