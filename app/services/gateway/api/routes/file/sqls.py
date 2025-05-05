from fastapi import APIRouter, Query, HTTPException, Header
from typing import List, Optional
from app.services.file.schemas.sqls import MetaInfoSchema
from app.common.clients.file_service_client import FileServiceClient
from app.core.config import settings
from app.services.log.tracing import get_tracer
from app.common.utils.auth_mode import get_auth_mode

tracer = get_tracer("gateway")

router = APIRouter(prefix="/file")
file_client = FileServiceClient(settings.FILE_SERVICE_URL)

@router.get(
    "/imgplt/sqls",
    response_model=List[MetaInfoSchema],
    tags=["File"],
    summary="SQL 기반 메타데이터 조회",
    description="사용자가 전달한 SQL을 실행하여 메타 정보를 반환합니다."
)
async def get_meta_sqls(
    query: str = Query(..., description="실행할 SQL 쿼리"),
    authorization: Optional[str] = Header(None, description="Bearer accessToken")
):
    

    if get_auth_mode() == "remote":
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Authorization header required")
        access_token = authorization.split(" ", 1)[1]
        headers = {"Authorization": f"Bearer {access_token}"}
    else:
        headers = {}
    try:
        result = await file_client._request(
            "GET", f"/imgplt/sqls?query={query}",
            headers=headers
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
