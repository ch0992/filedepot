from fastapi import APIRouter
from app.services.gateway.api.routes import file
from app.services.gateway.api.routes.auth import auths
from app.services.gateway.api.routes.data import topics as data_topics, curs as data_curs
from app.services.gateway.api.routes.log import events as log_events
from app.services.gateway.api.routes.internal import test_sentry
from app.services.gateway.api.routes.internal import log_test

router = APIRouter()
router.include_router(auths.router)
router.include_router(file.router)
router.include_router(data_topics.router)
router.include_router(data_curs.router)
router.include_router(log_events.router)
router.include_router(test_sentry.router)
router.include_router(log_test.router)

@router.get("/gateway/ping", summary="Gateway health check", tags=["Health"])
async def gateway_ping():
    """Gateway 서비스 헬스 체크 엔드포인트"""
    return {"message": "pong"}
