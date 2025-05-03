from pydantic import BaseModel
from typing import Optional

class FileMetadataRequest(BaseModel):
    file_id: str
    size: int
    user: Optional[str] = None

class KafkaProduceResult(BaseModel):
    topic: str
    message: str
    status: str  # e.g. "success" or "error"
