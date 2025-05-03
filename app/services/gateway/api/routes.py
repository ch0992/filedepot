"""
게이트웨이 서비스 API 라우터
"""
from fastapi import APIRouter

from app.services.gateway.api.routes.data import curs

router = APIRouter()
router.include_router(curs.router)

@router.get("/ping", summary="Health check", tags=["Health"])
async def ping():
    """헬스 체크 엔드포인트"""
    return {"message": "pong"}
