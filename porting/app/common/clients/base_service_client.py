import httpx
from abc import ABC, abstractmethod
from typing import Any, Dict
from fastapi import HTTPException
import asyncio

"""
[📄 base_service_client.py - Base Service Client]

설명:
- 모든 서비스 클라이언트의 공통 기능을 제공하는 베이스 클래스
- 서비스 간 통신, 인증, 예외처리 등의 기본 메서드를 정의
"""

class BaseServiceClient(ABC):
    """
    BaseServiceClient는 모든 서비스 클라이언트의 공통 기능을 제공하는 베이스 클래스입니다.
    
    Attributes:
    - base_url (str): 서비스 클라이언트의 기본 URL
    - timeout (float): 서비스 클라이언트의 타임아웃 시간 (기본값: 5.0초)
    - max_retries (int): 서비스 클라이언트의 최대 재시도 횟수 (기본값: 2회)
    """

    def __init__(self, base_url: str, timeout: float = 5.0, max_retries: int = 2):
        """
        BaseServiceClient의 생성자입니다.
        
        Args:
        - base_url (str): 서비스 클라이언트의 기본 URL
        - timeout (float): 서비스 클라이언트의 타임아웃 시간 (기본값: 5.0초)
        - max_retries (int): 서비스 클라이언트의 최대 재시도 횟수 (기본값: 2회)
        """
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries

    async def _request(self, method: str, path: str, **kwargs) -> Any:
        """
        BaseServiceClient의 내부 요청 메서드입니다.
        
        Args:
        - method (str): 요청 메서드 (예: GET, POST, PUT, DELETE)
        - path (str): 요청 경로
        - **kwargs: 추가 요청 파라미터
        
        Returns:
        - Any: 요청 결과
        """
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
