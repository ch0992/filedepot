from fastapi import APIRouter, HTTPException, Body, Header, status
from typing import Optional
from app.services.gateway.services.impl.data_cursor_service import DataCursorService
from app.services.gateway.services.impl.auth_module_service import AuthModuleService
from app.services.data.schemas.curs import CursorQueryRequest, CursorQueryResult

router = APIRouter(prefix="/data")
data_cursor_service = DataCursorService()
auth_service = AuthModuleService()

def _cursor_query_logic(request: CursorQueryRequest, authorization: Optional[str]):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header required")
    access_token = authorization.split(" ", 1)[1]
    # 인증 및 커서 쿼리 실행
    return auth_service.verify_token_and_get_workspaces(access_token).then(
        lambda _: data_cursor_service.cursor_query(request)
    )

from app.services.log.tracing import get_tracer
from app.services.log.exceptions import capture_and_log
import logging

@router.post(
    "/imgplt/curs",
    response_model=CursorQueryResult,
    tags=["data"],
    summary="Cursor 기반 대용량 레코드 조회",
    description="SQL 기반 대용량 데이터를 cursor 키를 기준으로 나누어 순차적으로 조회합니다."
)
async def cursor_query_imgplt(
    request: CursorQueryRequest = Body(...),
    authorization: Optional[str] = Header(None, description="Bearer accessToken")
):
    tracer = get_tracer("gateway")
    with tracer.start_as_current_span("gateway::cursor_query_imgplt"):
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header required")
        access_token = authorization.split(" ", 1)[1]
        try:
            await auth_service.verify_token_and_get_workspaces(access_token)
            result = await data_cursor_service.cursor_query(request)
            return result
        except Exception as e:
            logger = logging.getLogger("filedepot")
            capture_and_log(e, logger=logger)
            raise HTTPException(status_code=500, detail=str(e))

@router.post(
    "/curs",
    response_model=CursorQueryResult,
    tags=["data"],
    summary="Cursor 기반 대용량 레코드 조회",
    description="SQL 기반 대용량 데이터를 cursor 키를 기준으로 나누어 순차적으로 조회합니다."
)
async def cursor_query(
    request: CursorQueryRequest = Body(...),
    authorization: Optional[str] = Header(None, description="Bearer accessToken")
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header required")
    try:
        access_token = authorization.split(" ", 1)[1]
        await auth_service.verify_token_and_get_workspaces(access_token)
        result = await data_cursor_service.cursor_query(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
