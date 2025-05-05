from fastapi import APIRouter
from fastapi import Header, HTTPException
from . import sqls, s3, zips, topics, aliases, upload

router = APIRouter()
router.include_router(sqls.router)
router.include_router(s3.router)
router.include_router(zips.router)
router.include_router(topics.router)


@router.get("/aliases", summary="Alias 목록 조회", tags=["File"])
async def get_aliases(authorization: str = Header(..., description="Bearer accessToken")):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization header required")
    access_token = authorization.split(" ", 1)[1]
    try:
        result = await file_client._request(
            "GET", "/aliases",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

router.include_router(aliases.router)
router.include_router(upload.router)
