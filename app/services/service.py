from typing import List, Optional
from datetime import datetime
from app.domains.item import ItemIn, ItemOut, ItemFilters
from app.repositories.repository import AbstractRepository
from app.external.client import ExternalClient


class SyncService:
    def __init__(self, repo: AbstractRepository, external_client: ExternalClient):
        self.repo = repo
        self.external_client = external_client
    
    def sync(self, page: int = 1, limit: int = 50, since: str = None) -> int:
        items_data = self.external_client.get_items(
            page=page, 
            limit=limit, 
            since=since
        )
        
        items_in = [ItemIn(**item_dict) for item_dict in items_data]
        
        processed_data = [item.model_dump() for item in items_in]
        
        self.repo.upsert_many(processed_data)
        
        return len(items_data)


class ItemService:
    def __init__(self, repository: AbstractRepository):
        self.repository = repository
    
    def get_items(self, page: int = 1, limit: int = 50, since: Optional[str] = None) -> List[ItemIn]:
        since_dt = None
        if since:
            try:
                since_dt = datetime.fromisoformat(since)
            except ValueError:
                pass
        
        filters = ItemFilters(page=page, limit=limit, since=since_dt)
    
    def get_active_items(self, page: int = 1, limit: int = 50) -> List[ItemIn]:
        items = self.repository.get_items(ItemFilters(page=page, limit=limit))
        
        return [item for item in items if not item.is_deleted]