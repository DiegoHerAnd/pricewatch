from pydantic import BaseModel, field_validator, HttpUrl
from uuid import UUID

class ProductCreate(BaseModel):
    name:        str
    description: str | None = None
    brand:       str | None = None
    image_url:   str | None = None
    category_id: UUID

    @field_validator("name")
    def name_not_empty(cls, v):
        if not v.strip():
            raise ValueError("El nombre no puede estar vacío")
        return v.strip()

    @field_validator("image_url")
    def image_url_valid(cls, v):
        if v and not v.startswith("http"):
            raise ValueError("La URL debe empezar por http o https")
        return v

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