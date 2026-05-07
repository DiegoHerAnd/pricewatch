import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Text, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app import Base

class Product(Base):
    __tablename__ = "products"

    id:          Mapped[uuid.UUID]      = mapped_column(primary_key=True, default=uuid.uuid4)
    category_id: Mapped[uuid.UUID]      = mapped_column(ForeignKey("categories.id"), nullable=False)
    name:        Mapped[str]            = mapped_column(String(255), nullable=False)
    description: Mapped[str | None]     = mapped_column(Text)
    brand:       Mapped[str | None]     = mapped_column(String(100))
    image_url:   Mapped[str | None]     = mapped_column(Text)
    is_active:   Mapped[bool]           = mapped_column(Boolean, default=True)
    created_at:  Mapped[datetime]       = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at:  Mapped[datetime]       = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    category:           Mapped["Category"]          = relationship(back_populates="products")
    product_store_urls: Mapped[list["ProductStoreUrl"]] = relationship(back_populates="product")
    alerts:             Mapped[list["Alert"]]           = relationship(back_populates="product")