import httpx
from typing import List, Optional
from app.external.external import AbstractExternal


class ExternalClient(AbstractExternal):
    def __init__(self, base_url: str = "http://localhost:8000/external"):
        self.base_url = base_url
    
    def get_items(self, page: int, limit: int, since: Optional[str] = None) -> List[dict]:
        params = {"page": page, "limit": limit}
        if since:
            params["since"] = since
        
        with httpx.Client(base_url=self.base_url) as client:
            response = client.get("/items", params=params)
            response.raise_for_status()
            return response.json()