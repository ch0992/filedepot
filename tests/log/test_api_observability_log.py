import pytest
import os
from fastapi.testclient import TestClient
from app.services.gateway.main import app
import re
from app.services.log.tracing import TraceIdFormatter

@pytest.fixture(autouse=True, scope="session")
def set_otel_exporter_env():
    if "OTEL_EXPORTER" not in os.environ:
        os.environ["OTEL_EXPORTER"] = "none"

client = TestClient(app)

API_ENDPOINTS = [
    "/file/imgplt/aliases",
    "/imgplt/test/sentry",
    "/imgplt/log-test",
    "/internal-test/hello"
]

import pytest
import os
from fastapi.testclient import TestClient
from app.services.gateway.main import app
import re
from app.services.log.tracing import TraceIdFormatter

@pytest.fixture(autouse=True, scope="session")
def set_otel_exporter_env():
    if "OTEL_EXPORTER" not in os.environ:
        os.environ["OTEL_EXPORTER"] = "none"

client = TestClient(app)

API_TEST_CASES = [
    # (endpoint, method, kwargs)
    ("/file/imgplt/aliases", "GET", {"headers": {"Authorization": "Bearer test-access-token"}}),
    ("/file/imgplt/s3/test.txt", "GET", {"headers": {"Authorization": "Bearer test-access-token"}}),
    ("/file/imgplt/zips", "GET", {"headers": {"Authorization": "Bearer test-access-token"}, "params": {"sql": "SELECT * FROM files"}}),
    ("/file/imgplt/sqls", "GET", {"headers": {"Authorization": "Bearer test-access-token"}, "params": {"query": "SELECT * FROM files"}}),
    ("/file/topics/test-topic", "POST", {"headers": {"Authorization": "Bearer test-access-token"}, "json": {"field": "value"}}),
    ("/data/topics", "GET", {}),
    ("/data/topics/test-table", "POST", {"headers": {"Authorization": "Bearer test-access-token"}, "json": {"field": "value"}}),
    ("/data/sqls", "POST", {"headers": {"Authorization": "Bearer test-access-token"}, "json": {"sql": "SELECT * FROM data"}}),
    ("/data/curs", "POST", {"headers": {"Authorization": "Bearer test-access-token"}, "json": {"query": "SELECT * FROM data", "cursor": None}}),
    ("/auth/imgplt/auths", "GET", {"headers": {"Authorization": "Bearer test-access-token"}}),
    ("/log/event", "POST", {"headers": {"Authorization": "Bearer test-access-token"}, "json": {"event": "test-event"}}),
    ("/log/ping", "GET", {}),
    ("/file/ping", "GET", {}),
    ("/data/ping", "GET", {}),
    ("/imgplt/test/sentry", "GET", {"headers": {"Authorization": "Bearer test-access-token"}}),
    ("/imgplt/test-trace", "GET", {}),
    ("/imgplt/log-test", "GET", {}),
    ("/internal-test/hello", "GET", {}),
    ("/gateway/ping", "GET", {}),
]

@pytest.mark.parametrize("endpoint,method,kwargs", API_TEST_CASES)
def test_api_observability_log(endpoint, method, kwargs, caplog):
    caplog.set_level("INFO")
    # caplog 핸들러에 TraceIdFormatter 직접 적용
    caplog.handler.setFormatter(TraceIdFormatter("%(levelname)s %(trace_id)s %(span_id)s %(name)s:%(lineno)d %(message)s"))
    client_method = getattr(client, method.lower())
    response = client_method(endpoint, **kwargs)
    trace_found = False
    for record in caplog.records:
        # 로그 레코드 필드에 trace_id/ span_id 존재 및 값 체크
        if hasattr(record, "trace_id") and hasattr(record, "span_id"):
            if str(getattr(record, "trace_id")) != "-" and str(getattr(record, "span_id")) != "-":
                trace_found = True
                break
    # 헬스체크/단순 응답 API는 trace_id/ span_id 체크 제외
    health_check_endpoints = ["/internal-test/hello", "/log/ping", "/file/ping", "/data/ping", "/gateway/ping"]
    if endpoint in health_check_endpoints:
        assert response.status_code == 200
    else:
        assert trace_found, f"{endpoint} 로그에 trace_id/ span_id 미포함"
        assert response.status_code in (200, 500, 401)
    if endpoint in ["/imgplt/test/sentry"]:
        assert any("Exception captured" in r.getMessage() for r in caplog.records)

# 테스트 종료 후 TracerProvider shutdown (OpenTelemetry 익스포터 에러 방지)
import pytest
from opentelemetry import trace

@pytest.fixture(scope="session", autouse=True)
def shutdown_tracer_provider():
    yield
    provider = trace.get_tracer_provider()
    if hasattr(provider, "shutdown"):
        provider.shutdown()
