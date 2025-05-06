"""
pytest 기반 /ping API 테스트 (log 서비스)
"""
from fastapi.testclient import TestClient
from app.services.log.main import app

def test_ping():
    client = TestClient(app)
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"message": "pong"}
