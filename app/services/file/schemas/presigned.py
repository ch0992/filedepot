from pydantic import BaseModel

class PresignedURLResponse(BaseModel):
    url: str
    expires_in: int  # 만료 시간(초)
