"""
IMetaQueryService: 메타 데이터 질의 기능 인터페이스 정의
"""
from typing import Protocol
from pydantic import BaseModel

class MetaQueryRequest(BaseModel):
    query: str

class MetaQueryResponse(BaseModel):
    result: dict

class IMetaQueryService(Protocol):
    def query(self, req: MetaQueryRequest) -> MetaQueryResponse:
        ...
