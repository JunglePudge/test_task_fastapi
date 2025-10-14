from datetime import datetime
from pydantic import BaseModel


class ItemIn(BaseModel):
    id: int
    name: str
    updated_at: datetime
    is_deleted: bool = False


class ItemOut(BaseModel):
    id: int
    name: str
    updated_at: datetime