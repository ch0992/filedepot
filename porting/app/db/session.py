"""
app/db/session.py
SQLAlchemy 세션 관리 (placeholder)
"""

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

DATABASE_URL = os.getenv("DB_URL", "sqlite:///./test.db")
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
