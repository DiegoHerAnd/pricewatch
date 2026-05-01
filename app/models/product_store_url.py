import uuid
from datetime import datetime
from sqlalchemy import String, Text, Boolean, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class ProductStoreUrl(Base):
    __tablename__ = "product_store_urls"
    __table_args__ = (UniqueConstraint("product_id", "store_id"),)

    id:             Mapped[uuid.UUID]      = mapped_column(primary_key=True, default=uuid.uuid4)
    product_id:     Mapped[uuid.UUID]      = mapped_column(ForeignKey("products.id"), nullable=False)
    store_id:       Mapped[uuid.UUID]      = mapped_column(ForeignKey("stores.id"), nullable=False)
    url:            Mapped[str]            = mapped_column(Text, nullable=False)
    selector_price: Mapped[str | None]     = mapped_column(String(255))
    selector_name:  Mapped[str | None]     = mapped_column(String(255))
    is_active:      Mapped[bool]           = mapped_column(Boolean, default=True)
    last_checked:   Mapped[datetime | None]= mapped_column(DateTime(timezone=True))

    product:       Mapped["Product"] = relationship(back_populates="product_store_urls")
    store:         Mapped["Store"]   = relationship(back_populates="product_store_urls")
    price_history: Mapped[list["PriceHistory"]] = relationship(back_populates="product_store_url")