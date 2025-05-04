from opentelemetry.propagate import inject
from app.services.log.tracing import get_tracer
import requests

# 내부 서비스 호출 시 trace context를 HTTP 헤더에 포함시키는 유틸리티

def call_internal_service(url: str, method: str = "GET", data=None, headers=None, timeout=3):
    tracer = get_tracer("gateway-service")
    with tracer.start_as_current_span(f"gateway_internal_call:{url}"):
        _headers = headers.copy() if headers else {}
        inject(_headers)  # traceparent 등 W3C Trace Context 삽입
        if method.upper() == "GET":
            resp = requests.get(url, headers=_headers, timeout=timeout)
        elif method.upper() == "POST":
            resp = requests.post(url, json=data, headers=_headers, timeout=timeout)
        else:
            raise ValueError(f"Unsupported method: {method}")
        return resp
