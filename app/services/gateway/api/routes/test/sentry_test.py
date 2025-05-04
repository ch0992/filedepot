from fastapi import APIRouter, HTTPException
from app.services.log.exceptions import capture_and_log

router = APIRouter()

@router.get("/imgplt/test/sentry")
async def sentry_trigger():
    try:
        raise ValueError("\ud83d\udea8 Test error for Sentry")
    except Exception as e:
        import logging
        logger = logging.getLogger("filedepot")
        capture_and_log(e, logger=logger)
        raise HTTPException(status_code=500, detail="Test exception triggered")
