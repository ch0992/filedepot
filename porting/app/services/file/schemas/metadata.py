from pydantic import BaseModel
from typing import Optional

class FileMetadataRequest(BaseModel):
    file_id: str
    filename: str
    owner: str
    size: int
    user: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "file_id": "abc123",
                "filename": "test.png",
                "owner": "user1",
                "size": 12345
            }
        }

class KafkaProduceResult(BaseModel):
    topic: str
    message: str
    status: str  # e.g. "success" or "error"
