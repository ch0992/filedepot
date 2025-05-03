"""
로그 서비스 API 라우터
"""
from fastapi import APIRouter, Body

router = APIRouter()

@router.get("/ping", summary="Ping-pong API")
async def ping():
    """헬스 체크 및 테스트용 엔드포인트"""
    return {"message": "pong"}

@router.post("/event", summary="로그 이벤트 기록")
async def log_event(event: dict = Body(...)):
    return {"result": "logged", "event": event}
