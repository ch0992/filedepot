from fastapi import APIRouter, Query, HTTPException, Header
from app.services.gateway.services.impl.file_zip_service import FileZipService
from app.services.file.schemas.zips import ZipPresignedResponse

router = APIRouter()
file_zip_service = FileZipService()

from app.services.gateway.services.impl.auth_module_service import verify_access_token_dependency, auth_service
from fastapi import Depends

@router.get(
    "/imgplt/zips",
    response_model=ZipPresignedResponse,
    tags=["file"],
    summary="Presigned ZIP 다운로드 링크 생성",
    description="SQL 조건으로 대상 파일들을 조회하고, presigned zip 다운로드 링크를 생성해 반환합니다."
)
async def get_zip_presigned_url(
    sql: str = Query(..., description="SQL 조건"),
    authorization: str = Header(..., description="Bearer accessToken")
):
    from app.services.log.tracing import get_tracer
    from app.services.log.exceptions import capture_and_log
    import logging
    tracer = get_tracer("gateway")
    with tracer.start_as_current_span("gateway::get_zip_presigned_url"):
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Authorization header required")
        access_token = authorization.split(" ", 1)[1]
        await auth_service.verify_token_and_get_workspaces(access_token)
        try:
            result = await file_zip_service.create_zip_presigned_url(sql)
            return result
        except Exception as e:
            logger = logging.getLogger("filedepot")
            capture_and_log(e, logger=logger)
            raise HTTPException(status_code=400, detail=str(e))
