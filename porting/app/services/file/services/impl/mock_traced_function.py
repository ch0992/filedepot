import asyncio
from app.services.log.tracing import get_tracer

tracer = get_tracer("file")

async def mock_traced_function():
    with tracer.start_as_current_span("file::mock_process"):
        await asyncio.sleep(1)
        return "trace OK"
