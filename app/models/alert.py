import uuid
from datetime import datetime
from sqlalchemy import String, Boolean, ForeignKey, DateTime, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app import Base

class Alert(Base):
    __tablename__ = "alerts"

    id:           Mapped[uuid.UUID]      = mapped_column(primary_key=True, default=uuid.uuid4)
    product_id:   Mapped[uuid.UUID]      = mapped_column(ForeignKey("products.id"), nullable=False)
    store_id:     Mapped[uuid.UUID | None] = mapped_column(ForeignKey("stores.id"))
    target_price: Mapped[float]          = mapped_column(Numeric(12, 2), nullable=False)
    condition:    Mapped[str]            = mapped_column(String(20), default="below")
    is_active:    Mapped[bool]           = mapped_column(Boolean, default=True)
    triggered_at: Mapped[datetime | None]= mapped_column(DateTime(timezone=True))
    created_at:   Mapped[datetime]       = mapped_column(DateTime(timezone=True))

    product: Mapped["Product"]    = relationship(back_populates="alerts")
    store:   Mapped["Store | None"] = relationship(back_populates="alerts")