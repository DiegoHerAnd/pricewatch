from pydantic import BaseModel, field_validator
from uuid import UUID

class StoreCreate(BaseModel):
    name:     str
    base_url: str
    currency: str = "EUR"

    @field_validator("currency")
    def currency_valid(cls, v):
        allowed = ["EUR", "USD", "GBP"]
        if v.upper() not in allowed:
            raise ValueError(f"Divisa no soportada. Usa: {', '.join(allowed)}")
        return v.upper()

    @field_validator("base_url")
    def url_valid(cls, v):
        if not v.startswith("http"):
            raise ValueError("La URL debe empezar por http o https")
        return v

class StoreUpdate(BaseModel):
    name:      str | None = None
    base_url:  str | None = None
    is_active: bool | None = None

class StoreResponse(BaseModel):
    id:        UUID
    name:      str
    base_url:  str
    currency:  str
    is_active: bool

    model_config = {"from_attributes": True}