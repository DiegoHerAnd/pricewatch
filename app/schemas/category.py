from pydantic import BaseModel
from uuid import UUID

class CategoryCreate(BaseModel):
    name:        str
    slug:        str
    description: str | None = None
    parent_id:   UUID | None = None

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