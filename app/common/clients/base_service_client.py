import httpx
from abc import ABC, abstractmethod
from typing import Any, Dict
from fastapi import HTTPException
import asyncio

class BaseServiceClient(ABC):
    def __init__(self, base_url: str, timeout: float = 5.0, max_retries: int = 2):
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries

    async def _request(self, method: str, path: str, **kwargs) -> Any:
        url = self.base_url + path
        print(f"[ServiceClient] Request: {method} {url} | kwargs={kwargs}")
        for attempt in range(self.max_retries + 1):
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    response = await client.request(method, url, **kwargs)
                response.raise_for_status()
                print(f"[ServiceClient] Response: {response.status_code} {response.text}")
                return response.json()
            except (httpx.RequestError, httpx.HTTPStatusError) as e:
                print(f"[ServiceClient][ERROR] Attempt {attempt+1}/{self.max_retries+1}: {e} | type={type(e)}")
                if attempt < self.max_retries:
                    await asyncio.sleep(0.2 * (attempt + 1))
                    continue
                print(f"[ServiceClient][FAIL] Final failure for {method} {url}")
                raise HTTPException(status_code=502, detail=f"Service call failed: {e}")

    @abstractmethod
    async def health(self) -> Dict[str, Any]:
        pass
