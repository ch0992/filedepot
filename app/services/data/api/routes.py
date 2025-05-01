"""
데이터 서비스 API 라우터
"""
from fastapi import APIRouter, Depends
from app.services.data.schemas.ping import PingResponse

router = APIRouter()

@router.get("/ping", response_model=PingResponse, summary="Ping-pong API")
def ping():
    """헬스 체크 및 테스트용 엔드포인트"""
    return {"message": "pong"}
