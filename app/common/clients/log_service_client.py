from .base_service_client import BaseServiceClient

class LogServiceClient(BaseServiceClient):
    async def health(self):
        return await self._request("GET", "/ping")

    async def log_event(self, event: dict):
        return await self._request("POST", "/event", json=event)
