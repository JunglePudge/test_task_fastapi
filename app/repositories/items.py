from app.repositories.repository import SQLALchemyRepository
from app.models.items import Item


class ItemRepository(SQLALchemyRepository):
    model = Item