from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class PriceHistoryResponse(BaseModel):
    id:          UUID
    price:       float
    currency:    str
    in_stock:    bool
    scraped_at:  datetime

    model_config = {"from_attributes": True}

class PriceHistoryPaginated(BaseModel):
    total:  int
    page:   int
    limit:  int
    data:   list[PriceHistoryResponse]