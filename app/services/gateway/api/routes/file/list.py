from fastapi import APIRouter, Path, Header, status, HTTPException
from app.common.exceptions import NotFoundException, SystemConfigException
from typing import List, Optional
from app.services.file.schemas.listing import S3FileEntry
from app.services.gateway.services.impl.auth_module_service import auth_service
from app.common.utils.auth_mode import get_auth_mode
from app.core.logging import get_tracer, capture_and_log
from app.common.clients.file_service_client import FileServiceClient
from app.core.config import settings

file_client = FileServiceClient(settings.FILE_SERVICE_URL)

router = APIRouter()
tracer = get_tracer("gateway::list_files")

@router.get(
    "/imgplt/list/{prefix}",
    tags=["File"],
    summary="S3 prefix 기반 파일 리스트 조회",
    description="S3 버킷 내 지정된 prefix 하위의 파일 목록을 조회합니다.",
    response_model=List[S3FileEntry]
)
@capture_and_log(tracer)
async def list_files(
    prefix: str = Path(..., description="S3 prefix 경로"),
    authorization: Optional[str] = Header(None, description="Bearer accessToken")
):
    if get_auth_mode() == "remote":
        if not authorization or not authorization.startswith("Bearer "):
            raise UnauthorizedException("Authorization header required")
        access_token = authorization.split(" ", 1)[1]
        await auth_service.verify_token_and_get_workspaces(access_token)

    try:
        result = await file_client.list_files(prefix)
        return result
    except NotFoundException as e:
        raise
    except SystemConfigException as e:
        raise
    except HTTPException as e:
        raise
    except Exception as e:
        raise SystemConfigException(str(e))
