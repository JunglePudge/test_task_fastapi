from typing import Iterable, List, Optional
from datetime import datetime
from app.domains.item import ItemIn, ItemOut, ItemFilters
from app.repositories.repository import AbstractRepository

from typing import List
from datetime import datetime
from app.domains.item import ItemIn, ItemFilters


class FakeItemRepository:
    def __init__(self, fake_data: List[dict]):
        self.fake_data = fake_data
    
    def get_items(self, filters: ItemFilters) -> List[ItemIn]:
        items = self.fake_data.copy()
        
        if filters.since:
            items = self._filter_by_since(items, filters.since)
        
        start = (filters.page - 1) * filters.limit
        end = start + filters.limit
        paginated_items = items[start:end]
        
        return [ItemIn(**item) for item in paginated_items]
    
    def _filter_by_since(self, items: List[dict], since: datetime) -> List[dict]:
        filtered_items = []
        for item in items:
            try:
                item_updated_at = datetime.fromisoformat(item["updated_at"])
                if item_updated_at > since:
                    filtered_items.append(item)
            except Exception:
                filtered_items.append(item)
        return filtered_items