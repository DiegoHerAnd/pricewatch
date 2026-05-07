# app/models/category.py
import uuid
from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app import Base

class Category(Base):
    __tablename__ = "categories"

    id:          Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name:        Mapped[str]       = mapped_column(String(100), nullable=False)
    slug:        Mapped[str]       = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str | None]= mapped_column(Text)
    parent_id:   Mapped[uuid.UUID | None] = mapped_column(ForeignKey("categories.id"))

    products: Mapped[list["Product"]] = relationship(back_populates="category")