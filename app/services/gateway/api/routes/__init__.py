from fastapi import APIRouter
from app.services.gateway.api.routes import file
from app.services.gateway.api.routes import raise_test
from app.services.gateway.api.routes.auth import auths
from app.services.gateway.api.routes.data import topics as data_topics, curs as data_curs
from app.services.gateway.api.routes.log import events as log_events
from app.services.gateway.api.routes.internal import log_test_router, test_sentry_router, test_hello_router, test_trace_router
from app.services.gateway.api.routes.test import sentry_test

from fastapi.responses import JSONResponse
from fastapi.requests import Request

router = APIRouter()
router.include_router(auths.router)
router.include_router(file.router)
router.include_router(raise_test.router)
router.include_router(data_topics.router)
router.include_router(data_curs.router)
router.include_router(log_events.router)
router.include_router(test_sentry_router)
router.include_router(log_test_router)
router.include_router(test_hello_router)
router.include_router(test_trace_router)
# 테스트용 Sentry 트리거 엔드포인트
router.include_router(sentry_test.router)

@router.get("/ping", summary="Health check", tags=["Health"])
async def ping():
    # 실제 gateway 서비스 상태 반환 (예: version, uptime 등)
    return {"status": "ok", "service": "gateway"}
