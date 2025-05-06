from pydantic import BaseModel

class UploadResponse(BaseModel):
    filename: str
    status: str
    location: str = ""
    error: str = ""
    kafka_result: dict = None
