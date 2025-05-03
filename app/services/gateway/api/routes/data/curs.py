from fastapi import APIRouter, HTTPException, Body, Header, status
from typing import Optional
from app.services.gateway.services.impl.data_cursor_service import DataCursorService
from app.services.gateway.services.impl.auth_module_service import AuthModuleService
from app.services.data.schemas.curs import CursorQueryRequest, CursorQueryResult

router = APIRouter()
data_cursor_service = DataCursorService()
auth_service = AuthModuleService()

@router.post(
    "/imgplt/curs",
    response_model=CursorQueryResult,
    tags=["data"],
    summary="Cursor 기반 대용량 레코드 조회",
    description="SQL 기반 대용량 데이터를 cursor 키를 기준으로 나누어 순차적으로 조회합니다."
)
async def cursor_query_endpoint(
    request: CursorQueryRequest = Body(...),
    authorization: Optional[str] = Header(None, description="Bearer accessToken")
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header required")
    access_token = authorization.split(" ", 1)[1]
    await auth_service.verify_token_and_get_workspaces(access_token)
    try:
        result = await data_cursor_service.cursor_query(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
