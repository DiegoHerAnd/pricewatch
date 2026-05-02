from pydantic import BaseModel, HttpUrl
from uuid import UUID

class ProductCreate(BaseModel):
    name:        str
    description: str | None = None
    brand:       str | None = None
    image_url:   str | None = None
    category_id: UUID

class ProductUpdate(BaseModel):
    name:        str | None = None
    description: str | None = None
    brand:       str | None = None
    is_active:   bool | None = None

class ProductResponse(BaseModel):
    id:          UUID
    name:        str
    brand:       str | None
    is_active:   bool

    model_config = {"from_attributes": True}