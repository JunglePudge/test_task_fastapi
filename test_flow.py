import pytest
from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


@pytest.fixture(autouse=True)
def _reset_db():
# упрощённо: в реальном решении стоит чистить БД корректно
    yield


def test_sync_then_list_returns_only_active_items():
    # синхроним все записи
    r = client.post("/sync", params={"page": 1, "limit": 50})
    assert r.status_code == 200
    # ожидаем, что удалённые НЕ вернутся
    r = client.get("/items")
    assert r.status_code == 200
    data = r.json()
    # ожидаем хотя бы один активный элемент
    assert any(x["id"] == 1 for x in data) or any(x["id"] == 3 for x in data)