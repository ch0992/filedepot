"""
실행 가능한 FastAPI 앱 엔트리포인트
Swagger UI(/docs) 활성화, 환경설정 연동 예시 포함
"""
from fastapi import FastAPI, HTTPException
from app.services.data.api.routes import router as data_router
from app.core.config import settings
from app.services.log.middleware import install_exception_handlers, TraceLoggingMiddleware

app = FastAPI(title="Data Service", description="Meta info & SQL microservice")
install_exception_handlers(app)
app.add_middleware(TraceLoggingMiddleware)

app.include_router(data_router)
