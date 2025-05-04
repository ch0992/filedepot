import asyncio
from fastapi import APIRouter
from app.services.log.tracing import get_tracer
from app.services.file.services.impl.mock_traced_function import mock_traced_function

router = APIRouter()
tracer = get_tracer("gateway")

@router.get("/imgplt/test-trace", summary="Jaeger 트레이스 테스트", tags=["internal"], description="gateway → file 서비스 분산 추적 흐름 테스트")
async def test_trace():
    with tracer.start_as_current_span("gateway::test_trace"):
        result = await mock_traced_function()
        return {"result": result}
