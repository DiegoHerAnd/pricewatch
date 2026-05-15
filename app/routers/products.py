from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.models.product import Product
from datetime import datetime
from app.models.price_history import PriceHistory
from app.models.product_store_url import ProductStoreUrl
from app.schemas.price_history import PriceHistoryPaginated
from app.core.limiter import limiter

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/{product_id}/prices",
            response_model=PriceHistoryPaginated,
            summary = "Historial de precios",
            description = "Devuelve el historial de precios de un producto con soporte de filtros por tienda, rango de fecchas y paginación."
            )
@limiter.limit("30/minute")
def get_price_history(
    request: Request,
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

@router.get("/",
            response_model=list[ProductResponse],
            summary = "Listar productos",
            description = "Devuelve todos los productos activos registrados en el sistema."
            )
@limiter.limit("30/minute")
def get_products(request: Request, db: Session = Depends(get_db)):
    return db.query(Product).filter(Product.is_active == True).all()

@router.get("/{product_id}",
            response_model=ProductResponse,
            summary = "Obtener productos",
            description = "Devuelve el detalle de un producto concreto por su ID."
            )
@limiter.limit("30/minute")
def get_product(request: Request, product_id: str, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product

@router.post("/",
             response_model=ProductResponse,
             status_code=201,
             summary = "Crear producto",
             description = "Registra un nuevo producto asociado a una categoría existente."
             )
@limiter.limit("10/minute")
def create_product(request: Request, data: ProductCreate, db: Session = Depends(get_db)):
    product = Product(**data.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

@router.put("/{product_id}",
            response_model=ProductResponse,
            summary = "Actualizar producto",
            description = "Actualiza los campos de un producto existente. Solo se modifican los campos enviados."
            )
@limiter.limit("10/minute")
def update_product(request: Request, product_id: str, data: ProductUpdate, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(product, key, value)
    db.commit()
    db.refresh(product)
    return product

@router.delete("/{product_id}",
               status_code=204,
               summary ="Eliminar producto",
               description = "Desactiva un producto (soft delete). No se borra físicamente de la base de datos."
               )
@limiter.limit("5/minute")
def delete_product(request: Request, product_id: str, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    product.is_active = False   # soft delete, no borrado real
    db.commit()