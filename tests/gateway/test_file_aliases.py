import pytest
from fastapi.testclient import TestClient
from app.services.gateway.main import app

client = TestClient(app)

def test_aliases_auth_required():
    response = client.get("/imgplt/aliases")
    assert response.status_code == 401
    assert response.json()["detail"] == "Authorization header required"

def test_aliases_success(monkeypatch):
    # 인증 모듈과 file 서비스 mock
    async def mock_verify_token_and_get_workspaces(token):
        return {"user": "test-user"}
    async def mock_get_aliases(self, user_info):
        return [
            {"alias": "project-a", "description": "프로젝트 A 적재 경로"},
            {"alias": "project-b", "description": "프로젝트 B 적재 경로"}
        ]
    from app.services.gateway.services.impl.auth_module_service import auth_service
    from app.services.gateway.services.impl.file_alias_service import FileAliasService
    monkeypatch.setattr(auth_service, "verify_token_and_get_workspaces", mock_verify_token_and_get_workspaces)
    monkeypatch.setattr(FileAliasService, "get_aliases", mock_get_aliases)
    response = client.get("/imgplt/aliases", headers={"Authorization": "Bearer test-access-token"})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data[0]["alias"] == "project-a"
    assert data[1]["alias"] == "project-b"
