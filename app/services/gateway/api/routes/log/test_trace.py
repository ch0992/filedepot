from fastapi import APIRouter
from app.services.log.tracing import get_tracer
from app.services.file.services.impl.mock_traced_function import mock_traced_function
from app.core.config import settings
from app.common.utils.auth_mode import get_auth_mode
from typing import Optional
from fastapi import Header
from fastapi import HTTPException

router = APIRouter()
tracer = get_tracer("gateway")

@router.get("/imgplt/test-trace", summary="Jaeger 트레이스 테스트", tags=["Log"], description="gateway → file 서비스 분산 추적 흐름 테스트")
async def test_trace(authorization: Optional[str] = Header(None, description="Bearer accessToken")):
    if get_auth_mode() == "remote":
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Authorization header required")
        access_token = authorization.split(" ", 1)[1]
    with tracer.start_as_current_span("gateway::test_trace"):
        result = await mock_traced_function()
        return {"result": result}
