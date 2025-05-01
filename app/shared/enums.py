"""
app/shared/enums.py
공통 Enum 정의 (placeholder)
"""
from enum import Enum

class ServiceType(str, Enum):
    FILE = "file"
    DATA = "data"
    LOG = "log"
    GATEWAY = "gateway"
