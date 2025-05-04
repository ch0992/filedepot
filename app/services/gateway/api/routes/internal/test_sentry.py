from fastapi import APIRouter, HTTPException
from app.services.log.exceptions import capture_and_log

router = APIRouter()

@router.get(
    "/imgplt/test-sentry",
    tags=["internal", "test"],
    summary="Sentry 테스트 예외 발생",
    description="OpenTelemetry 기반 예외 추적 로직이 Sentry로 예외를 전송하는지 확인합니다."
)
async def test_sentry():
    try:
        raise ValueError("💥 테스트용 예외 발생!")
    except Exception as e:
        capture_and_log(e)
        raise HTTPException(status_code=500, detail="Sentry 테스트 예외 전송됨")
