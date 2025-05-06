"""
app/shared/models.py
공통 Pydantic 모델 (placeholder)
"""
from pydantic import BaseModel

class HealthResponse(BaseModel):
    status: str
