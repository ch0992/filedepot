from pydantic import BaseModel

class KafkaProduceResult(BaseModel):
    topic: str
    status: str
    message: str
