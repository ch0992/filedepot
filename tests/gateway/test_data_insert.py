import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_insert_data_success(monkeypatch):
    class DummyService:
        async def insert(self, table, payload):
            return {"status": "queued", "topic": f"iceberg-insert-{table}"}
    
    monkeypatch.setattr("app.services.gateway.services.impl.data_insert_service.DataInsertService", DummyService)
    response = client.post(
        "/imgplt/topics/my_table",
        headers={"Authorization": "Bearer test-access-token"},
        json={"id": 1, "value": "example"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "queued"
    assert response.json()["topic"] == "iceberg-insert-my_table"
