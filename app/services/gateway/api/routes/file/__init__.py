from fastapi import APIRouter
from . import sqls, s3, zips, topics, aliases

router = APIRouter()
router.include_router(sqls.router)
router.include_router(s3.router)
router.include_router(zips.router)
router.include_router(topics.router)
router.include_router(aliases.router)
