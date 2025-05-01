"""
실행 가능한 FastAPI 앱 엔트리포인트
Swagger UI(/docs) 활성화, 환경설정 연동 예시 포함
"""
from fastapi import FastAPI
from app.services.gateway.api.routes import router as gateway_router
from app.core.config import settings

app = FastAPI(title="Gateway Service", description="Auth/JWT gateway microservice")
app.include_router(gateway_router)
