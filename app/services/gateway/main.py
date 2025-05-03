"""
실행 가능한 FastAPI 앱 엔트리포인트
Swagger UI(/docs) 활성화, 환경설정 연동 예시 포함
"""
import os
from dotenv import load_dotenv

# 반드시 .env를 import보다 먼저 로드 (경로 고정)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
ENV_PATH = os.path.join(BASE_DIR, '.env')
load_dotenv(ENV_PATH, override=True)
print("[gateway] AUTH_MODE (from .env):", os.environ.get("AUTH_MODE"))

from fastapi import FastAPI
from app.services.gateway.api.routes import router as gateway_router
from app.core.config import settings

tags_metadata = [
    {"name": "auth", "description": "인증 관련 API"},
    {"name": "data", "description": "데이터 관련 API"},
    {"name": "file", "description": "파일 관련 API"},
    {"name": "log", "description": "로그 관련 API"},
    {"name": "Health", "description": "헬스 체크 API"},
]

app = FastAPI(
    title="Gateway Service",
    description="Auth/JWT gateway microservice",
    openapi_tags=tags_metadata
)
app.include_router(gateway_router)

import logging

@app.on_event("startup")
def print_auth_mode():
    mode = os.environ.get("AUTH_MODE")
    local_token = os.environ.get("AUTH_LOCAL_TOKEN")
    remote_url = os.environ.get("AUTH_SERVER_URL")
    logging.basicConfig(level=logging.INFO)
    logging.info(f"[gateway] AUTH_MODE={mode}")
    if mode == "local" and local_token:
        logging.info(f"[gateway] AUTH_LOCAL_TOKEN={local_token}")
    elif mode == "remote":
        logging.info(f"[gateway] AUTH_SERVER_URL={remote_url}")

# 진단용: 실제 등록된 모든 라우트 경로와 메서드 출력
for route in app.routes:
    print(route.path, route.methods)
