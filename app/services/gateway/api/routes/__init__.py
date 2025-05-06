from fastapi import APIRouter
from app.services.gateway.api.routes.file.list import router as file_list_router
from app.services.gateway.api.routes import file
from app.services.gateway.api.routes.auth import auths
from app.services.gateway.api.routes.data import topics as data_topics, curs as data_curs
from app.services.gateway.api.routes.log import router as log_router
from app.services.gateway.api.routes.test import sentry_test


router = APIRouter()
router.include_router(file_list_router)
router.include_router(auths.router)
router.include_router(file.router)
router.include_router(data_topics.router)
router.include_router(data_curs.router)
router.include_router(log_router)
router.include_router(sentry_test.router)

@router.get("/ping", summary="Health check", tags=["Health"])
async def ping():
    # 실제 gateway 서비스 상태 반환 (예: version, uptime 등)
    return {"status": "ok", "service": "gateway"}
