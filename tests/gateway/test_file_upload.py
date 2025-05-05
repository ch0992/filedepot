import pytest
from fastapi.testclient import TestClient
from app.main import app
import io

client = TestClient(app)

def test_file_upload():
    file_content = b"test file content"
    metadata = '{"file_id":"abc123","user_id":"kim01","timestamp":"2024-01-01T10:00:00"}'
    files = {
        "file": ("test.jpg", io.BytesIO(file_content), "image/jpeg"),
        "metadata": (None, metadata)
    }
    response = client.post(
        "/imgplt/upload/test-topic",
        files=files,
        headers={"Authorization": "Bearer test-access-token"}
    )
    assert response.status_code == 200
    assert response.json()["upload_result"]["status"] == "uploaded"
