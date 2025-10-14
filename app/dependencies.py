from datetime import datetime, timedelta
from app.repositories.external import FakeItemRepository
from app.repositories.items import ItemRepository
from app.external.client import ExternalClient
from app.services.service import ItemService, SyncService

_FAKE_DATA = [
    {"id": 1, "name": "alpha", "updated_at": (datetime.utcnow() - timedelta(days=2)).isoformat(), "is_deleted": True},
    {"id": 2, "name": "beta", "updated_at": (datetime.utcnow() - timedelta(days=1)).isoformat(), "is_deleted": False},
    {"id": 3, "name": "gamma", "updated_at": (datetime.utcnow()).isoformat(), "is_deleted": False},
    {"id": 4, "name": "delta", "updated_at": (datetime.utcnow()).isoformat(), "is_deleted": False},
    {"id": 5, "name": "omega", "updated_at": (datetime.utcnow()).isoformat(), "is_deleted": True},
    {"id": 6, "name": "epsilon", "updated_at": (datetime.utcnow()).isoformat(), "is_deleted": True},
]

def get_fake_repository():
    return FakeItemRepository(_FAKE_DATA)

def get_fake_item_service():
    repository = get_fake_repository()
    return ItemService(repository)

def get_item_repository():
    return ItemRepository()

def get_external_client():
    return ExternalClient(base_url="http://localhost:8000/external")

def get_sync_service():
    return SyncService(
        repo=get_item_repository(),
        external_client=get_external_client()
    )