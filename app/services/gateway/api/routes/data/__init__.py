from fastapi import APIRouter
from app.services.gateway.api.routes.data import topics, curs, sqls

router = APIRouter()
router.include_router(topics.router)
router.include_router(curs.router)
router.include_router(sqls.router)
