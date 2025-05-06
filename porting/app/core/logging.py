"""
app/core/logging.py
공통 로깅 설정
"""

import logging
from functools import wraps
from opentelemetry import trace
from opentelemetry.trace import Tracer
import sentry_sdk
import sys
import traceback


def setup_logging():
    logging.basicConfig(level=logging.INFO)
    logging.info("Logging is configured.")

def get_tracer(service_name: str = "default") -> Tracer:
    try:
        return trace.get_tracer(service_name)
    except Exception:
        logging.warning("OpenTelemetry tracer unavailable, returning dummy tracer.")
        class DummySpan:
            def __enter__(self): return self
            def __exit__(self, exc_type, exc_val, exc_tb): pass
            def set_attribute(self, *a, **kw): pass
            def record_exception(self, *a, **kw): pass
        class DummyTracer:
            def start_as_current_span(self, name): return DummySpan()
        return DummyTracer()

def capture_and_log(tracer: Tracer):
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            span_name = func.__module__ + "." + func.__name__
            with tracer.start_as_current_span(span_name) as span:
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    logging.error(f"[capture_and_log] {span_name}: {e}")
                    span.record_exception(e)
                    sentry_sdk.capture_exception(e)
                    raise
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            span_name = func.__module__ + "." + func.__name__
            with tracer.start_as_current_span(span_name) as span:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logging.error(f"[capture_and_log] {span_name}: {e}")
                    span.record_exception(e)
                    sentry_sdk.capture_exception(e)
                    raise
        if func.__code__.co_flags & 0x80:  # async
            return async_wrapper
        else:
            return sync_wrapper
    return decorator
