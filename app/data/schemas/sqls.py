from pydantic import BaseModel, Field
from typing import List, Any

class SQLsQueryRequest(BaseModel):
    query: str = Field(..., description="실행할 SQL 쿼리")

class Metadata(BaseModel):
    column: str
    type: str
    sample: Any

class SQLsQueryResponse(BaseModel):
    items: List[Metadata]
