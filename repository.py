from typing import Iterable, List
from sqlalchemy import select
from sqlalchemy.orm import Session
from db import Item


class ItemRepository:
    def __init__(self, session: Session):
        self.session = session

    def upsert_many(self, items: Iterable[dict]):
        for d in items:
            obj = self.session.get(Item, d["id"]) or Item(id=d["id"])
            obj.name = d["name"]
            obj.updated_at = d["updated_at"]
            self.session.add(obj)

    def list_active(self) -> List[Item]:
        stmt = select(Item).where(Item.is_deleted == True)
        return list(self.session.execute(stmt).scalars())