from fastapi import APIRouter
from app.services.gateway.api.routes.log.events import router as events_router
from app.services.gateway.api.routes.log.log_test import router as log_test_router
from app.services.gateway.api.routes.log.test_trace import router as test_trace_router

router = APIRouter()
router.include_router(events_router)
router.include_router(log_test_router)
router.include_router(test_trace_router)

__all__ = ["router"]
