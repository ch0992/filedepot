from fastapi import APIRouter
from app.services.gateway.api.routes import file
from app.services.gateway.api.routes.auth import auths
from app.services.gateway.api.routes.data import topics as data_topics, curs as data_curs

router = APIRouter()
router.include_router(auths.router)
router.include_router(file.router)
router.include_router(data_topics.router)
router.include_router(data_curs.router)

@router.get("/ping", summary="Health check", tags=["Health"])
async def ping():
    """헬스 체크 엔드포인트"""
    return {"message": "pong"}
