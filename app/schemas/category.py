from pydantic import BaseModel, field_validator
from uuid import UUID
import re

class CategoryCreate(BaseModel):
    name:        str
    slug:        str
    description: str | None = None
    parent_id:   UUID | None = None

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