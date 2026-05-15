from pydantic import BaseModel, Field, field_validator, HttpUrl
from uuid import UUID

class ProductCreate(BaseModel):
    name:        str         = Field(example="Larry Carlton L7 BK")
    description: str | None  = Field(default=None, example="Guitarra eléctrica semiacústica")
    brand:       str | None  = Field(default=None, example="Larry Carlton")
    image_url:   str | None  = Field(default=None, example="https://www.thomann.es/larry_carlton_l7_bk_new_gen.htm")
    category_id: UUID        = Field(example="dce8654b-958e-4865-a49e-3ce55ffd9b71")

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