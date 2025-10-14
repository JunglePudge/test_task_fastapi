from typing import Optional
from fastapi import Depends, FastAPI
from app.domains.item import ItemIn
from app.services.service import ItemService
from app.dependencies import get_fake_item_service

fake_api = FastAPI(title="FakeAPI")

@fake_api.get("/items",
              response_model=list[ItemIn])
def list_items(
    page: int = 1,
    limit: int = 50,
    since: Optional[str] = None,
    service: ItemService = Depends(get_fake_item_service)
):
    res = service.get_items(page=page, limit=limit, since=since)
    return res
