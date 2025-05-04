"""
실행 가능한 FastAPI 앱 엔트리포인트
Swagger UI(/docs) 활성화, 환경설정 연동 예시 포함
"""
import os
from dotenv import load_dotenv
from fastapi import FastAPI

# .env 파일 로드 (상위 루트 기준)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
ENV_PATH = os.path.join(BASE_DIR, '.env')
load_dotenv(ENV_PATH, override=True)
print("[gateway] AUTH_MODE (from .env):", os.environ.get("AUTH_MODE"))

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

# OpenTelemetry 초기화
init_tracer(os.getenv("OTEL_EXPORTER", "stdout"))

# Sentry 초기화
init_sentry(dsn=os.getenv("SENTRY_DSN", ""), environment=os.getenv("ENV", "dev"))

# 예외 핸들러 및 미들웨어 등록
install_exception_handlers(app)
app.add_middleware(TraceLoggingMiddleware)

# 라우터 등록
gateway_router.tags = ["gateway"]
app.include_router(gateway_router)

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
