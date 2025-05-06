from .base_service_client import BaseServiceClient

"""
[📄 log_service_client.py - Log Service Client]

설명:
- 로그 관련 서비스와 통신하는 클라이언트
- 로그 수집, 전송, 예외처리 로직 포함
"""

class LogServiceClient(BaseServiceClient):
    async def health(self):
        return await self._request("GET", "/ping")

    async def log_event(self, event: dict):
        return await self._request("POST", "/event", json=event)
