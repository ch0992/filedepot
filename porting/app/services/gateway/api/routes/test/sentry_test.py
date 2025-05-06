from fastapi import APIRouter, HTTPException
from app.services.log.exceptions import capture_and_log
from opentelemetry import trace

router = APIRouter()
tracer = trace.get_tracer("gateway")

@router.get(
    "/imgplt/test-sentry",
    tags=["Log"],
    summary="Sentry 예외 트리거 테스트",
    description="OpenTelemetry 기반 예외 추적 로직이 Sentry로 예외를 전송하는지 검증합니다. 운영 연동 점검용.")
async def sentry_trigger():
    import logging
    logger = logging.getLogger("filedepot")
    try:
        with tracer.start_as_current_span("gateway::test_sentry") as span:
            raise ValueError("🚨 테스트용 예외 발생!")
    except Exception as e:
        capture_and_log(e, span, logger=logger)
        raise HTTPException(status_code=500, detail="Sentry 테스트 예외 전송됨")

