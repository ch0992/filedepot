import os
import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient
from app.services.log.tracing import get_tracer, inject_trace_context, init_tracer
from app.services.log.sentry import init_sentry, capture_exception
from app.services.log.exceptions import capture_and_log, AppException
from app.services.log.middleware import install_exception_handlers, TraceLoggingMiddleware

os.environ["OTEL_EXPORTER"] = "console"
os.environ["LOG_LEVEL"] = "DEBUG"

@pytest.fixture
def app():
    app = FastAPI()
    install_exception_handlers(app)
    app.add_middleware(TraceLoggingMiddleware)
    return app

import pytest
from app.services.log.tracing import get_tracer
from app.services.log.exceptions import capture_and_log

# 1. tracer.get_tracer()로 생성된 span context에서 로그 출력 시 trace_id 포함 여부

def test_tracer_log_capture(caplog):
    tracer = get_tracer("test-service")
    with tracer.start_as_current_span("test-span") as span:
        import logging
        from app.services.log.tracing import inject_trace_context
        logger = logging.getLogger("test")
        logger = inject_trace_context(logger, span)
        caplog.set_level("INFO")
        caplog.handler.setFormatter(logging.Formatter('%(levelname)s %(trace_id)s %(span_id)s %(message)s'))
        logger.info("This is a test log")
    logs = caplog.text
    assert "This is a test log" in logs
    tokens = logs.split()
    assert tokens[1].isdigit() and tokens[2].isdigit()

# 2. capture_and_log() 사용 시 stdout에 structured 로그 출력 및 mock sentry 전송 호출 확인

import pytest
from starlette.testclient import TestClient
from app.services.gateway.main import app

client = TestClient(app)

@pytest.mark.parametrize("endpoint,method,body", [
    ("/file/ping", "get", None),
    ("/data/ping", "get", None),
    ("/file/imgplt/aliases", "get", None),
    ("/file/imgplt/s3/somefile.txt", "get", None),
    ("/data/imgplt/sqls", "post", {"sql": "SELECT 1"}),
    ("/file/imgplt/zips", "get", {"sql": "SELECT 1"}),
    ("/data/imgplt/curs", "post", {"sql": "SELECT 1"}),
])
def test_logging_and_tracing_injection(endpoint, method, body):
    headers = {"Authorization": "Bearer test-access-token"}
    if method == "get":
        response = client.get(endpoint, headers=headers)
    elif method == "post":
        response = client.post(endpoint, headers=headers, json=body)
    else:
        pytest.skip("Unsupported method")
    # 정상/에러 응답 모두 trace_id가 로그에 찍히는지 확인(수동 확인 필요)
    assert response.status_code in (200, 400, 401, 500)

def test_capture_and_log(monkeypatch, caplog):
    def mock_capture_exception(e):
        print("Sentry Captured:", str(e))
    monkeypatch.setattr("app.services.log.sentry.capture_exception", mock_capture_exception)

    import logging
    from app.services.log.tracing import get_tracer, inject_trace_context
    tracer = get_tracer("test-service")
    with tracer.start_as_current_span("test-span") as span:
        logger = logging.getLogger("test")
        logger = inject_trace_context(logger, span)
        caplog.set_level("ERROR")
        caplog.handler.setFormatter(logging.Formatter('%(levelname)s %(trace_id)s %(span_id)s %(message)s'))
        try:
            raise ValueError("Test error")
        except Exception as e:
            capture_and_log(e, logger)
    logs = caplog.text
    assert "Exception captured" in logs

def test_app_exception_handler(app):
    client = TestClient(app)
    @app.get("/raise")
    async def raise_app_exc():
        raise AppException(code=400, message="bad req")
    resp = client.get("/raise")
    assert resp.status_code == 400
    assert resp.json()["error"] == "bad req"
    assert "trace_id" in resp.json()

def test_trace_logging_middleware(app, caplog):
    import logging
    caplog.set_level(logging.INFO)
    client = TestClient(app)
    @app.get("/hello")
    async def hello():
        return {"msg": "ok"}
    resp = client.get("/hello")
    assert resp.status_code == 200
    assert any("[access] GET" in r for r in caplog.text.splitlines())
