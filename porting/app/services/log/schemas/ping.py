"""
/ping 응답 모델
"""
from pydantic import BaseModel

class PingResponse(BaseModel):
    message: str
