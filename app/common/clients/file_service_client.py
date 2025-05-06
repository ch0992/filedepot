from .base_service_client import BaseServiceClient

class FileServiceClient(BaseServiceClient):
    async def health(self):
        return await self._request("GET", "/ping")

    async def get_aliases(self, user_id: str):
        return await self._request("GET", f"/aliases?user_id={user_id}")

    async def list_files(self, prefix: str):
        return await self._request("GET", f"/imgplt/list/{prefix}")
