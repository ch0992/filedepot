from fastapi import APIRouter, Query, HTTPException, Header
from typing import List
from app.services.file.schemas.sqls import MetaInfoSchema
from app.common.clients.file_service_client import FileServiceClient
from app.core.config import settings

router = APIRouter(prefix="/file")
file_client = FileServiceClient(settings.FILE_SERVICE_URL)

@router.get(
    "/imgplt/sqls",
    response_model=List[MetaInfoSchema],
    tags=["file"],
    summary="SQL 기반 메타데이터 조회",
    description="사용자가 전달한 SQL을 실행하여 메타 정보를 반환합니다."
)
async def get_meta_sqls(
    query: str = Query(..., description="실행할 SQL 쿼리"),
    authorization: str = Header(..., description="Bearer accessToken")
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization header required")
    access_token = authorization.split(" ", 1)[1]
    try:
        result = await file_client._request(
            "GET", f"/imgplt/sqls?query={query}",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
