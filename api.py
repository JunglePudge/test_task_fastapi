from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import SessionLocal, init_db
from repository import ItemRepository
from service import SyncService
from domain import ItemOut
from external import ExternalClient


router = APIRouter()


init_db()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/items", response_model=list[ItemOut])
def list_items(db: Session = Depends(get_db)):
    repo = ItemRepository(db)
    rows = repo.list_active()
    return [ItemOut.model_validate(r.__dict__) for r in rows]


@router.post("/sync")
def sync(page: int = 1, limit: int = 50, since: str | None = None, db: Session = Depends(get_db)):
    repo = ItemRepository(db)
    svc = SyncService(repo)
    client = ExternalClient(base_url="http://localhost:8000/external")
    items = client.get_items(page=page, limit=limit, since=since)
    svc.sync(items)
    return {"synced": len(items)}