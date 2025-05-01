"""
app/core/logging.py
공통 로깅 설정
"""

import logging

def setup_logging():
    logging.basicConfig(level=logging.INFO)
    logging.info("Logging is configured.")
