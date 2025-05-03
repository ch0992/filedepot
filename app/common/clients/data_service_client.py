from .base_service_client import BaseServiceClient

class DataServiceClient(BaseServiceClient):
    async def health(self):
        return await self._request("GET", "/ping")

    async def get_topics(self):
        return await self._request("GET", "/topics")
