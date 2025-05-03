"""
데이터 서비스 API 라우터
"""
from fastapi import APIRouter, Depends, Path, Body
from app.services.data.schemas.ping import PingResponse

router = APIRouter()

@router.get("/ping", response_model=PingResponse, summary="Ping-pong API")
async def ping():
    """헬스 체크 및 테스트용 엔드포인트"""
    return {"message": "pong"}

@router.get("/topics", summary="토픽 목록 조회")
async def get_topics():
    # 실제로는 DB 등에서 토픽 목록 조회
    return ["topic-a", "topic-b"]

@router.post("/topics/{table}", summary="토픽 데이터 적재")
async def produce_table_record_to_kafka(
    table: str = Path(..., description="Kafka 토픽명"),
    body: dict = Body(...)
):
    # 실제로는 DB/Kafka 등에 데이터 적재
    return {"result": "success", "table": table, "data": body}
