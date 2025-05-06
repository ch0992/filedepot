from pydantic import BaseModel

class TableRecordRequest(BaseModel):
    # 예시 필드, 실제 Mart 테이블 구조에 따라 변경
    order_id: str
    user_id: str
    amount: int
    # 기타 컬럼은 Dict 등으로 확장 가능
    # extra: Dict[str, Any] = {}

class KafkaProduceResult(BaseModel):
    topic: str
    message: str
    status: str
