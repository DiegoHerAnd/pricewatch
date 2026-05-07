import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Boolean, ForeignKey, DateTime, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class PriceHistory(Base):
    __tablename__ = "price_history"

    id:                   Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    product_store_url_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("product_store_urls.id"), nullable=False)
    price:                Mapped[float]     = mapped_column(Numeric(12, 2), nullable=False)
    currency:             Mapped[str]       = mapped_column(String(3), default="EUR")
    in_stock:             Mapped[bool]      = mapped_column(Boolean, default=True)
    scraped_status:       Mapped[str]       = mapped_column(String(50), default="success")
    scraped_at:           Mapped[datetime]  = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    product_store_url: Mapped["ProductStoreUrl"] = relationship(back_populates="price_history")