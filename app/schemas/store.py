from pydantic import BaseModel
from uuid import UUID

class StoreCreate(BaseModel):
    name:     str
    base_url: str
    currency: str = "EUR"

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