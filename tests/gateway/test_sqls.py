import pytest
from fastapi.testclient import TestClient
from app.gateway.api.routes.data.sqls import router
from fastapi import FastAPI

app = FastAPI()
app.include_router(router)

client = TestClient(app)

def test_sqls_success():
    resp = client.get("/imgplt/sqls", params={"query": "SELECT * FROM meta_table"})
    assert resp.status_code == 200
    data = resp.json()
    assert "items" in data
    assert isinstance(data["items"], list)
    assert len(data["items"]) > 0

def test_sqls_fail():
    resp = client.get("/imgplt/sqls", params={"query": "fail"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["items"] == []
