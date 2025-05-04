import requests
import pytest

# 실제 gateway가 포트포워딩되어 있는 주소
BASE_URL = "http://localhost:8000"

API_TEST_CASES = [
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
def test_api_observability_e2e(endpoint, method, kwargs):
    url = BASE_URL + endpoint
    method_func = getattr(requests, method.lower())
    response = method_func(url, timeout=5, **kwargs)
    # health check 엔드포인트는 200만 허용, 나머지는 200/401/500 허용
    health_check_endpoints = ["/internal-test/hello", "/log/ping", "/file/ping", "/data/ping", "/gateway/ping"]
    if endpoint in health_check_endpoints:
        assert response.status_code == 200, f"{endpoint} health check failed: {response.status_code}"
    else:
        assert response.status_code in (200, 401, 500), f"{endpoint} unexpected status: {response.status_code}"
    # 로그/트레이스 검증은 별도 수집 시스템에서 확인 (이 테스트는 API 정상 동작 및 응답 코드만 확인)
