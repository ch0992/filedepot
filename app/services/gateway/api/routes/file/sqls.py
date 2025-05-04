from fastapi import APIRouter, Query, HTTPException, Header
from typing import List
from app.services.gateway.services.impl.file_sqls_service import FileSqlsService
from app.services.gateway.services.impl.auth_module_service import auth_service
from app.services.file.schemas.sqls import MetaInfoSchema

router = APIRouter(prefix="/file")
file_sqls_service = FileSqlsService()

from app.services.gateway.services.impl.auth_module_service import verify_access_token_dependency
from fastapi import Depends

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
    from app.services.log.tracing import get_tracer
    from app.services.log.exceptions import capture_and_log
    import logging
    tracer = get_tracer("gateway")
    with tracer.start_as_current_span("gateway::get_meta_sqls"):
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Authorization header required")
        access_token = authorization.split(" ", 1)[1]
        await auth_service.verify_token_and_get_workspaces(access_token)
        try:
            result = await file_sqls_service.query_metadata(query)
            return result
        except Exception as e:
            logger = logging.getLogger("filedepot")
            capture_and_log(e, logger=logger)
            raise HTTPException(status_code=400, detail=str(e))
