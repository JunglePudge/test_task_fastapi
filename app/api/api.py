from fastapi import APIRouter, Depends
from app.dependencies import get_item_repository, get_sync_service
from app.domains.item import ItemOut
from app.repositories.repository import AbstractRepository
from app.services.service import SyncService

router = APIRouter()

@router.get("/items", response_model=list[ItemOut])
def list_items(repo: AbstractRepository = Depends(get_item_repository)):
    rows = repo.list_active()
    return [ItemOut.model_validate(r.__dict__) for r in rows]

@router.post("/sync")
def sync(
    page: int = 1, 
    limit: int = 50, 
    since: str = None,
    sync_service: SyncService = Depends(get_sync_service)
):
    synced_count = sync_service.sync(page=page, limit=limit, since=since)
    return {"synced": synced_count}