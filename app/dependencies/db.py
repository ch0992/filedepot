"""
app/dependencies/db.py
DB 세션 Depends 정의 (placeholder)
"""
from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
