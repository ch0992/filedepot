from app.services.gateway.services.impl import internal_call

def test_traceparent_header_injected(monkeypatch):
    """
    call_internal_service 호출 시 traceparent header가 포함되는지 확인
    """
    called = {}
    def fake_requests_get(url, headers=None, timeout=None):
        called['headers'] = headers
        class Resp:
            def json(self):
                return {'ok': True}
        return Resp()
    monkeypatch.setattr("requests.get", fake_requests_get)
    internal_call.call_internal_service("http://file-service/test-api")
    headers = called['headers']
    # traceparent가 실제로 헤더에 포함되어 있는지 확인
    assert any(k.lower() == 'traceparent' for k in headers)
    # W3C Trace Context 규격 확인
    traceparent = [v for k, v in headers.items() if k.lower() == 'traceparent']
    assert traceparent and traceparent[0].startswith('00-')

# 실제 서비스 간 연동 테스트는 통합테스트에서 수행해야 함
