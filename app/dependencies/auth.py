"""
app/dependencies/auth.py
공통 인증 Depends (placeholder)
"""
from fastapi import Depends, HTTPException

def get_current_user():
    # 실제 구현 필요
    raise HTTPException(status_code=401, detail="Not implemented")
