from fastapi import APIRouter
from app.services.log.tracing import get_tracer
import logging

logger = logging.getLogger(__name__)
tracer = get_tracer("gateway")

router = APIRouter(prefix="/imgplt")

@router.get("/log-test", summary="로그 OpenTelemetry-OpenSearch 연동 테스트", tags=["internal"], description="구조화 로그가 trace_id, span_id와 함께 OpenSearch에 적재되는지 검증.")
async def log_test():
    with tracer.start_as_current_span("gateway::log_test"):
        logger.info("✅ FileDepot log test executed!", extra={"service": "gateway", "module": "log_test", "user_id": "minwoo123"})
        return {"status": "log emitted"}
