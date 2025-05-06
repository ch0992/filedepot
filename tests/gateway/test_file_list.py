import pytest
from fastapi.testclient import TestClient
from app.services.gateway.main import app

client = TestClient(app)

def test_list_files_unauthorized():
    response = client.get("/imgplt/list/uploads/2025/")
    assert response.status_code == 401

def test_list_files_authorized(monkeypatch):
    dummy_result = [
        {
            "key": "uploads/2025/file1.png",
            "size": 123456,
            "last_modified": "2025-05-06T10:00:00"
        }
    ]

    async def dummy_list_files(self, prefix):
        return dummy_result

    monkeypatch.setattr(
        "app.services.gateway.services.impl.file_list_service.FileListService.list_files",
        dummy_list_files
    )

    response = client.get(
        "/imgplt/list/uploads/2025/",
        headers={"Authorization": "Bearer test-access-token"}
    )
    assert response.status_code == 200
    assert response.json() == dummy_result
