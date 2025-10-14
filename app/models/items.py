from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, Boolean, String, DateTime
from app.db.db import Base


class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    updated_at: Mapped[DateTime] = mapped_column(DateTime)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
