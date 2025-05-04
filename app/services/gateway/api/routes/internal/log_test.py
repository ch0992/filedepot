from fastapi import APIRouter, HTTPException
from app.services.log.tracing import get_tracer
import logging

logger = logging.getLogger(__name__)
tracer = get_tracer("gateway")

router = APIRouter()

@router.get("/imgplt/log-test", summary="로그 OpenTelemetry-OpenSearch 연동 테스트", tags=["internal"], description="구조화 로그가 trace_id, span_id와 함께 OpenSearch에 적재되는지 검증.")
async def log_test():
    try:
        logger.info(f"tracer type: {type(tracer)}")
        if tracer is None:
            logger.error("tracer is None!")
            raise HTTPException(status_code=500, detail="tracer is None!")
        with tracer.start_as_current_span("gateway::log_test"):
            logger.info("✅ FileDepot log test executed!", extra={"service": "gateway", "log_module": "log_test", "user_id": "minwoo123"})
            return {"status": "log emitted"}
    except Exception as e:
        logger.exception("log_test API 예외 발생: %s", e)
        raise HTTPException(status_code=500, detail=f"Internal Error: {e}")
