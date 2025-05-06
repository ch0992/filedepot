"""
실행 가능한 FastAPI 앱 엔트리포인트
Swagger UI(/docs) 활성화, 환경설정 연동 예시 포함
"""
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from app.services.log.tracing import init_tracer
from app.services.log.sentry import init_sentry
from app.services.log.middleware import install_exception_handlers, TraceLoggingMiddleware
from app.services.file.api.routes import router as file_router
from app.core.config import settings
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

# .env 파일 로드 (상위 루트 기준)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
ENV_PATH = os.path.join(BASE_DIR, '.env')
load_dotenv(ENV_PATH, override=True)

app = FastAPI(title="File Service", description="File upload/download microservice")

# OpenTelemetry 및 Sentry 초기화 (ENV에 따라 분기)
if settings.ENV in ["production", "stage"]:
    if settings.OTEL_EXPORTER:
        init_tracer(settings.OTEL_EXPORTER)
    if settings.USE_SENTRY and settings.SENTRY_DSN:
        init_sentry(dsn=settings.SENTRY_DSN, environment=settings.ENV)
else:
    # 개발/테스트 환경: OTEL, Sentry는 stdout 또는 mock
    init_tracer("stdout")
    # Sentry 미연동 또는 dummy

# OpenTelemetry FastAPI 미들웨어 적용
FastAPIInstrumentor().instrument_app(app)

# 예외 핸들러 및 미들웨어 등록
install_exception_handlers(app)
app.add_middleware(TraceLoggingMiddleware)

# 라우터 등록
app.include_router(file_router)
