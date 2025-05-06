"""
게이트웨이 서비스 API 라우터
"""
from fastapi import APIRouter

from app.services.gateway.api.routes.data import curs
from app.common.clients.file_service_client import FileServiceClient
from app.common.clients.data_service_client import DataServiceClient
from app.common.clients.log_service_client import LogServiceClient
from app.core.config import settings
from app.services.log.tracing import get_tracer

router = APIRouter()
router.include_router(curs.router)

file_client = FileServiceClient(settings.FILE_SERVICE_URL)
data_client = DataServiceClient(settings.DATA_SERVICE_URL)
log_client = LogServiceClient(settings.LOG_SERVICE_URL)
tracer = get_tracer("gateway")

@router.get("/ping", summary="Health check", tags=["Health"])
async def ping():
    return {"message": "pong"}

@router.get("/file/ping", summary="File service health check", tags=["Health"])
async def file_ping():
    return {"message": "pong"}

@router.get("/data/ping", summary="Data service health check", tags=["Health"])
async def data_ping():
    return {"message": "pong"}

@router.get("/log/ping", summary="Log service health check", tags=["Health"])
async def log_ping():
    return {"message": "pong"}

