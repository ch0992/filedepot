"""
데이터 서비스 API 라우터
"""
import json
from fastapi import APIRouter, Path, Body, HTTPException
from app.services.data.schemas.ping import PingResponse
from app.services.data.schemas.kafka import KafkaProduceResult
from app.common.utils.auth_mode import get_auth_mode

router = APIRouter()

@router.get("/ping", response_model=PingResponse, summary="Ping-pong API")
async def ping():
    print("[DATA] /ping called")
    """헬스 체크 및 테스트용 엔드포인트"""
    return {"message": "pong"}

@router.get("/topics", summary="토픽 목록 조회")
async def get_topics():
    print("[DATA] /topics called")
    # 실제로는 DB 등에서 토픽 목록 조회
    return ["topic-a", "topic-b"]

@router.post("/imgplt/curs", summary="Cursor 기반 대용량 레코드 조회")
async def cursor_query_endpoint(body: dict = Body(...)):
    # 실제로는 DB에서 커서 기반 쿼리 처리
    # 예시 응답
    return {
        "rows": [
            {"id": 1, "value": "row1"},
            {"id": 2, "value": "row2"}
        ],
        "next_cursor": None
    }

@router.post("/topics/{table}", summary="토픽 데이터 적재", response_model=KafkaProduceResult)
async def produce_table_record_to_kafka(
    table: str = Path(..., description="Kafka 토픽명"),
    body: dict = Body(...)
):
    if get_auth_mode() == "remote":
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Authorization header required")
        access_token = authorization.split(" ", 1)[1]
        headers = {"Authorization": f"Bearer {access_token}"}
    else:
        headers = {}
    print(f"[DATA] /topics/{{table}} called")
    # 실제로는 DB/Kafka 등에 데이터 적재
    return {"topic": table, "status": "success", "message": json.dumps(body)}
