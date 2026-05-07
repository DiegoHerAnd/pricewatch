from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.models.product import Product
from datetime import datetime
from app.models.price_history import PriceHistory
from app.models.product_store_url import ProductStoreUrl
from app.schemas.price_history import PriceHistoryPaginated

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/{product_id}/prices", response_model=PriceHistoryPaginated)
def get_price_history(
    product_id: str,
    store_id:  str | None = None,      # ?store_id=uuid
    from_date: datetime | None = None, # ?from_date=2024-01-01
    to_date:   datetime | None = None, # ?to_date=2024-12-31
    page:      int = 1,
    limit:     int = 20,
    db: Session = Depends(get_db)
):
    query = (
        db.query(PriceHistory)
        .join(ProductStoreUrl)
        .filter(ProductStoreUrl.product_id == product_id)
    )

    if store_id:
        query = query.filter(ProductStoreUrl.store_id == store_id)
    if from_date:
        query = query.filter(PriceHistory.scraped_at >= from_date)
    if to_date:
        query = query.filter(PriceHistory.scraped_at <= to_date)

    total  = query.count()
    data   = (query
              .order_by(PriceHistory.scraped_at.desc())
              .offset((page - 1) * limit)
              .limit(limit)
              .all())

    return {"total": total, "page": page, "limit": limit, "data": data}

@router.get("/", response_model=list[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).filter(Product.is_active == True).all()

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: str, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product

@router.post("/", response_model=ProductResponse, status_code=201)
def create_product(data: ProductCreate, db: Session = Depends(get_db)):
    product = Product(**data.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: str, data: ProductUpdate, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(product, key, value)
    db.commit()
    db.refresh(product)
    return product

@router.delete("/{product_id}", status_code=204)
def delete_product(product_id: str, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    product.is_active = False   # soft delete, no borrado real
    db.commit()