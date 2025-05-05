from fastapi import APIRouter, Depends, Header, HTTPException, status, Request
from fastapi.responses import JSONResponse
from typing import Any, Dict
from app.services.gateway.services.impl.data_insert_service import DataInsertService
from app.services.gateway.schemas.insert_payload import InsertPayload
from app.services.gateway.auth import get_current_user
from app.services.log.exceptions import capture_and_log
from opentelemetry import trace
from app.core.config import settings
from typing import Optional
from app.common.utils.auth_mode import get_auth_mode
    
router = APIRouter()
tracer = trace.get_tracer("gateway")

@router.post(
    "/imgplt/topics/{table}",
    summary="Kafka 기반 단건 데이터 적재",
    description="단건 JSON 데이터를 Kafka로 발행한 후 Flink를 통해 Iceberg에 적재하는 구조입니다.",
    tags=["Data"],
    response_model=Dict[str, Any],
)
async def insert_single(
    table: str,
    payload: InsertPayload,
    request: Request,
    authorization: str = Header(..., alias="Authorization"),
    current_user: dict = Depends(get_current_user),
):
    if get_auth_mode() == "remote":
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Authorization header required")
        access_token = authorization.split(" ", 1)[1]
        await auth_service.verify_token_and_get_workspaces(access_token)
    try:
        with tracer.start_as_current_span("gateway.insert_single") as span:
            result = await DataInsertService().insert(table, payload.dict())
            span.set_attribute("kafka.topic", result["topic"])
            return {"status": "queued", "topic": result["topic"]}
    except Exception as e:
        capture_and_log(e, trace.get_current_span())
        raise HTTPException(status_code=500, detail="Failed to queue data for insert.")
