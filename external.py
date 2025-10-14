import httpx
from typing import List
from domain import ItemIn


class ExternalClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self._client = httpx.Client(base_url=base_url, timeout=5)

    def get_items(self,
                  page: int = 1,
                  limit: int = 50,
                  since: str | None = None) -> List[ItemIn]:
        params = {
            "page": page,
            "limit": limit
        }
        if since:
            params["since"] = since
        resp = self._client.get("/items", params=params)
        resp.raise_for_status()
        return [ItemIn(**x) for x in resp.json()]

# Фейковый внешний API (монтируется в основном приложении как /external)
from datetime import datetime, timedelta
from fastapi import FastAPI
from fastapi.responses import JSONResponse

fake_api = FastAPI()

_FAKE = [
    {"id": 1, "name": "alpha", "updated_at": (datetime.utcnow() - timedelta(days=2)).isoformat(), "is_deleted": False},
    {"id": 2, "name": "beta", "updated_at": (datetime.utcnow() - timedelta(days=1)).isoformat(), "is_deleted": True},
    {"id": 3, "name": "gamma", "updated_at": (datetime.utcnow()).isoformat(), "is_deleted": False},
    {"id": 4, "name": "delta", "updated_at": (datetime.utcnow()).isoformat(), "is_deleted": True},
    {"id": 5, "name": "omega", "updated_at": (datetime.utcnow()).isoformat(), "is_deleted": False},
    {"id": 6, "name": "epsilon", "updated_at": (datetime.utcnow()).isoformat(), "is_deleted": True},
]


@fake_api.get("/items")
def list_items(page: int = 1, limit: int = 50, since: str | None = None):
    items = _FAKE[:]
    if since:
        try:
            dt = datetime.fromisoformat(since)
            items = [x for x in items if datetime.fromisoformat(x["updated_at"]) > dt]
        except Exception:
            pass
    start = (page - 1) * limit
    end = start + limit
    return JSONResponse(items[start:end])
