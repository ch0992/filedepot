"""
IAuthService: 인증/인가(JWT) 기능 인터페이스 정의
"""
from typing import Protocol
from pydantic import BaseModel

class AuthRequest(BaseModel):
    token: str

class AuthResponse(BaseModel):
    valid: bool
    user_id: str = None

class IAuthService(Protocol):
    def verify(self, req: AuthRequest) -> AuthResponse:
        ...
