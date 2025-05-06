"""
실행 가능한 FastAPI 앱 엔트리포인트
Swagger UI(/docs) 활성화, 환경설정 연동 예시 포함
"""
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

from app.services.log.tracing import init_tracer, patch_global_logging_format
from app.services.log.sentry import init_sentry
from app.services.log.middleware import install_exception_handlers, TraceLoggingMiddleware
from app.services.gateway.api.routes import router as gateway_router

# 글로벌 로그 포맷터 패치(최상단에 적용)
patch_global_logging_format()

# .env 파일 로드 (상위 루트 기준)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
ENV_PATH = os.path.join(BASE_DIR, '.env')
load_dotenv(ENV_PATH, override=True)
print("[gateway] AUTH_MODE (from .env):", os.environ.get("AUTH_MODE"))

tags_metadata = [
    {"name": "Auth", "description": "인증 관련 API"},
    {"name": "Data", "description": "데이터 관련 API"},
    {"name": "File", "description": "파일 관련 API"},
    {"name": "Log", "description": "로그 관련 API"},
    {"name": "Health", "description": "헬스 체크 API"}
]

app = FastAPI(
    title="Gateway Service",
    description="Auth/JWT gateway microservice",
    openapi_tags=tags_metadata,
    openapi_url="/gateway/openapi.json",
    docs_url="/gateway/docs",
    redoc_url="/gateway/redoc"
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
app.include_router(gateway_router, prefix="/gateway")

import logging
import sys
import traceback
from fastapi.responses import JSONResponse
from fastapi import Request

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    import logging
    from fastapi import HTTPException
    from app.common.exceptions import SystemConfigException
    logger = logging.getLogger("gateway-exception")
    # Sentry 연동
    global SENTRY_ENABLED, SENTRY_DSN
    if SENTRY_ENABLED and SENTRY_DSN:
        try:
            import sentry_sdk
            sentry_sdk.capture_exception(exc)
        except Exception as sentry_exc:
            logger.error(f"[Sentry] 연동 실패: {sentry_exc}")
    # 상세 로깅
    logger.error(f"[Global Exception Handler] {request.method} {request.url} - {exc}", exc_info=True)
    # HTTPException은 FastAPI가 자체 처리하므로 여기선 생략
    # 커스텀 SystemConfigException 등은 그대로 반환
    if isinstance(exc, HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )
    # 기타 미처리 예외는 500으로 통일
    return JSONResponse(
        status_code=500,
        content={"detail": "예상치 못한 오류가 발생했습니다.", "error": str(exc)},
    )

@app.on_event("startup")
async def on_startup():
    mode = os.environ.get("AUTH_MODE")
    local_token = os.environ.get("AUTH_LOCAL_TOKEN")
    remote_url = os.environ.get("AUTH_SERVER_URL")
    logging.basicConfig(level=logging.INFO)
    logging.info("Gateway service started.")
    logging.info(f"[gateway] AUTH_MODE={mode}")
    if mode == "local" and local_token:
        logging.info(f"[gateway] AUTH_LOCAL_TOKEN={local_token}")
    elif mode == "remote":
        logging.info(f"[gateway] AUTH_SERVER_URL={remote_url}")

# 진단용: 실제 등록된 모든 라우트 경로와 메서드 출력
for route in app.routes:
    print(route.path, route.methods)

from fastapi.responses import JSONResponse
from fastapi.requests import Request


