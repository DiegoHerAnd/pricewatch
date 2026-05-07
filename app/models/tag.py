import uuid
from sqlalchemy import String, Column, Table, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base

# Tabla intermedia muchos a muchos
product_tags = Table(
    "product_tags",
    Base.metadata,
    Column("product_id", ForeignKey("products.id"), primary_key=True),
    Column("tag_id",     ForeignKey("tags.id"),     primary_key=True),
)

class Tag(Base):
    __tablename__ = "tags"

    id:    Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name:  Mapped[str]       = mapped_column(String(50), nullable=False, unique=True)
    color: Mapped[str]       = mapped_column(String(7), default="#6B7280")