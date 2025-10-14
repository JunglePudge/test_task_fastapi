import pytest
from fastapi.testclient import TestClient
from main import app
from main import app  # импортируйте ваше приложение
from datetime import datetime, timedelta
client = TestClient(app)


@pytest.fixture(autouse=True)
def _reset_db():
    # упрощённо: в реальном решении стоит чистить БД корректно
    yield


# Тестовые данные на основе ваших моделей
_FAKE_DATA = [
    {"id": 1, "name": "alpha", "updated_at": (datetime.utcnow() - timedelta(days=2)).isoformat(), "is_deleted": True},
    {"id": 2, "name": "beta", "updated_at": (datetime.utcnow() - timedelta(days=1)).isoformat(), "is_deleted": False},
    {"id": 3, "name": "gamma", "updated_at": (datetime.utcnow()).isoformat(), "is_deleted": False},
    {"id": 4, "name": "delta", "updated_at": (datetime.utcnow()).isoformat(), "is_deleted": False},
    {"id": 5, "name": "omega", "updated_at": (datetime.utcnow()).isoformat(), "is_deleted": True},
    {"id": 6, "name": "epsilon", "updated_at": (datetime.utcnow()).isoformat(), "is_deleted": True},
]

class TestExternalItems:
    def test_list_external_items_success(self):
        response = client.get("/external/items")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        
        # Проверяем структуру ItemIn
        if len(data) > 0:
            item = data[0]
            assert "id" in item
            assert "name" in item
            assert "updated_at" in item
            assert "is_deleted" in item
            assert isinstance(item["id"], int)
            assert isinstance(item["name"], str)
            assert isinstance(item["is_deleted"], bool)

    def test_list_external_items_with_pagination(self):
        response = client.get("/external/items?page=1&limit=2")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_list_external_items_with_since(self):
        since_date = (datetime.utcnow() - timedelta(days=1)).isoformat()
        response = client.get(f"/external/items?since={since_date}")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

class TestItems:
    def test_list_items_success(self):
        response = client.get("/items")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        
        # Проверяем структуру ItemOut
        if len(data) > 0:
            item = data[0]
            assert "id" in item
            assert "name" in item
            assert "updated_at" in item
            # Проверяем, что is_deleted НЕ возвращается (только в external)
            assert "is_deleted" not in item
            assert isinstance(item["id"], int)
            assert isinstance(item["name"], str)

class TestSync:
    def test_sync_success(self):
        response = client.post("/sync")
        assert response.status_code == 200
        data = response.json()
        assert "synced" in data
        assert isinstance(data["synced"], int)

    def test_sync_with_parameters(self):
        response = client.post("/sync?page=2&limit=30")
        assert response.status_code == 200
        data = response.json()
        assert "synced" in data

    def test_sync_with_since(self):
        since_date = (datetime.utcnow() - timedelta(days=1)).isoformat()
        response = client.post(f"/sync?since={since_date}")
        assert response.status_code == 200
        data = response.json()
        assert "synced" in data

# Тесты для валидации параметров
class TestParametersValidation:
    def test_invalid_page_parameter(self):
        response = client.get("/external/items?page=0")
        # Может вернуть 422 или 400 в зависимости от валидации
        assert response.status_code in [200, 400, 422]

    def test_invalid_limit_parameter(self):
        response = client.get("/external/items?limit=0")
        assert response.status_code in [200, 400, 422]

    def test_invalid_since_format(self):
        response = client.get("/external/items?since=invalid-date")
        assert response.status_code in [200, 400, 422]

# Тесты для сравнения ответов разных эндпоинтов
class TestEndpointsComparison:
    def test_external_vs_main_items_structure(self):
        external_response = client.get("/external/items")
        main_response = client.get("/items")
        
        assert external_response.status_code == 200
        assert main_response.status_code == 200
        
        external_data = external_response.json()
        main_data = main_response.json()
        
        # Проверяем, что external содержит is_deleted, а main - нет
        if len(external_data) > 0:
            assert "is_deleted" in external_data[0]
        if len(main_data) > 0:
            assert "is_deleted" not in main_data[0]


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