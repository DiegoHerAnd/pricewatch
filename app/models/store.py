import uuid
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class Store(Base):
    __tablename__ = "stores"

    id:         Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name:       Mapped[str]       = mapped_column(String(100), nullable=False, unique=True)
    base_url:   Mapped[str]       = mapped_column(String(255), nullable=False)
    currency:   Mapped[str]       = mapped_column(String(3), default="EUR")
    is_active:  Mapped[bool]      = mapped_column(Boolean, default=True)

    product_store_urls: Mapped[list["ProductStoreUrl"]] = relationship(back_populates="store")
    alerts:             Mapped[list["Alert"]]           = relationship(back_populates="store")