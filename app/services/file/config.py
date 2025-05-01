"""
환경설정 예시: .env 기반 설정을 core.config(Settings)에서 불러와 사용
서비스별 추가 설정이 필요하면 이 파일에서 관리
"""
from app.core.config import settings

# 예시: 서비스별 설정
FILE_STORAGE_PATH = getattr(settings, "FILE_STORAGE_PATH", "/data/files")
