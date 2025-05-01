"""
ILogCollectService: 로그 수집 기능 인터페이스 정의
"""
from typing import Protocol
from pydantic import BaseModel

class LogCollectRequest(BaseModel):
    start_time: str
    end_time: str
    filter: str = None

class LogCollectResponse(BaseModel):
    logs: list

class ILogCollectService(Protocol):
    def collect(self, req: LogCollectRequest) -> LogCollectResponse:
        ...
