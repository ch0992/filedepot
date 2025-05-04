import os
import sys
import logging
import importlib
import pytest
from unittest import mock

from app.services.log import tracing, sentry, exceptions

def test_get_tracer_no_env(monkeypatch):
    # OTEL_EXPORTER 환경 변수 제거
    monkeypatch.delenv("OTEL_EXPORTER", raising=False)
    tracer = tracing.get_tracer("test-service")
    # fallback-safe: tracer는 항상 객체 반환 (NoOpTracer 포함)
    assert tracer is not None
    assert hasattr(tracer, "start_as_current_span")

def test_init_tracer_no_exception(monkeypatch):
    monkeypatch.delenv("OTEL_EXPORTER", raising=False)
    try:
        tracing.init_tracer()
    except Exception as e:
        pytest.fail(f"init_tracer raised: {e}")

def test_capture_exception_no_sentry(monkeypatch, caplog):
    monkeypatch.delenv("SENTRY_DSN", raising=False)
    caplog.set_level(logging.WARNING)
    with caplog.at_level(logging.WARNING):
        sentry.capture_exception(Exception("test error"))
    assert any("SENTRY_DSN 미설정" in r.message for r in caplog.records)

def test_capture_and_log_fallback(monkeypatch, caplog):
    monkeypatch.delenv("SENTRY_DSN", raising=False)
    caplog.set_level(logging.ERROR)
    logger = logging.getLogger("test")
    try:
        exceptions.capture_and_log(Exception("fallback test error"), logger=logger)
    except Exception as e:
        pytest.fail(f"capture_and_log raised: {e}")
    # 에러 로그가 찍혔는지 확인
    assert any("Exception captured" in r.message for r in caplog.records)
