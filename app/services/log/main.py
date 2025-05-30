"""
실행 가능한 FastAPI 앱 엔트리포인트
Swagger UI(/docs) 활성화, 환경설정 연동 예시 포함
"""
from fastapi import FastAPI
from app.services.log.api.routes import router as log_router
from app.core.config import settings
from app.services.log.middleware import install_exception_handlers, TraceLoggingMiddleware

app = FastAPI(title="Log Service", description="API log microservice")
install_exception_handlers(app)
app.add_middleware(TraceLoggingMiddleware)
app.include_router(log_router)
