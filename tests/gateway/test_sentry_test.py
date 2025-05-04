from fastapi.testclient import TestClient
from app.services.gateway.main import app

client = TestClient(app)

def test_sentry_trigger():
    response = client.get("/imgplt/test/sentry")
    assert response.status_code == 500
    assert response.json()["detail"] == "Test exception triggered"
