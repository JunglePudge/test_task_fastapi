from typing import Iterable, List
from sqlalchemy import select
from app.db.db import SessionLocal
from abc import ABC, abstractmethod

class AbstractRepository(ABC):
    @abstractmethod
    def upsert_many():
        raise NotImplemented
    
    @abstractmethod
    def list_active():
        raise NotImplemented


class SQLALchemyRepository(AbstractRepository):
    model = None
    
    def upsert_many(self, data: Iterable[dict]):
        with SessionLocal() as session:
            for item_data in data:
                obj = session.get(self.model, item_data["id"])
                
                if obj:
                    for key, value in item_data.items():
                        if hasattr(obj, key):
                            setattr(obj, key, value)
                else:
                    obj = self.model(**item_data)
                    session.add(obj)
            
            session.commit()


    def list_active(self):
        with SessionLocal() as session:
            stmt = (select(self.model)
                    .where(self.model.is_deleted == False))
            result = session.execute(stmt)
            return list(result.scalars())
    


