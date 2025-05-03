from pydantic import BaseModel
from typing import List

class ZipPresignedResponse(BaseModel):
    presigned_url: str
    files: List[str]
    sql: str
