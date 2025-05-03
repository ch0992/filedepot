from pydantic import BaseModel, StrictStr
from typing import List, Optional, Any

class CursorQueryRequest(BaseModel):
    query: StrictStr
    cursor: Optional[str] = None

class CursorQueryResult(BaseModel):
    records: List[Any]
    next_cursor: Optional[str] = None
