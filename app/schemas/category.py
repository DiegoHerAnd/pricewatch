from pydantic import BaseModel, Field, field_validator
from uuid import UUID
import re

class CategoryCreate(BaseModel):
    name:        str            = Field(example="Guitarras")
    slug:        str            = Field(example="guitarras")
    description: str | None     = Field(default=None, example="Guitarras eléctricas y acústicas")
    parent_id:   UUID | None    = Field(default=None, example=None)

    @field_validator("slug")
    def slug_format(cls, v):
        if not re.match(r'^[a-z0-9]+(?:-[a-z0-9]+)*$', v):
            raise ValueError("El slug solo puede contener minúsculas, números y guiones")
        return v

class CategoryUpdate(BaseModel):
    name:        str | None = None
    description: str | None = None

class CategoryResponse(BaseModel):
    id:          UUID
    name:        str
    slug:        str
    description: str | None
    parent_id:   UUID | None

    model_config = {"from_attributes": True}