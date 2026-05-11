from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.schemas.store import StoreCreate, StoreUpdate, StoreResponse
from app.models.store import Store
from app.core.limiter import limiter

router = APIRouter(prefix="/stores", tags=["Stores"])

@router.get("/", response_model=list[StoreResponse])
@limiter.limit("30/minute")
def get_stores(request: Request, db: Session = Depends(get_db)):
    return db.query(Store).filter(Store.is_active == True).all()

@router.get("/{store_id}", response_model=StoreResponse)
@limiter.limit("30/minute")
def get_store(request: Request, store_id: str, db: Session = Depends(get_db)):
    store = db.query(Store).filter(Store.id == store_id).first()
    if not store:
        raise HTTPException(status_code=404, detail="Tienda no encontrada")
    return store

@router.post("/", response_model=StoreResponse, status_code=201)
@limiter.limit("10/minute")
def create_store(request: Request, data: StoreCreate, db: Session = Depends(get_db)):
    store = Store(**data.model_dump())
    db.add(store)
    db.commit()
    db.refresh(store)
    return store

@router.put("/{store_id}", response_model=StoreResponse)
@limiter.limit("10/minute")
def update_store(request: Request, store_id: str, data: StoreUpdate, db: Session = Depends(get_db)):
    store = db.query(Store).filter(Store.id == store_id).first()
    if not store:
        raise HTTPException(status_code=404, detail="Tienda no encontrada")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(store, key, value)
    db.commit()
    db.refresh(store)
    return store

@router.delete("/{store_id}", status_code=204)
@limiter.limit("5/minute")
def delete_store(request: Request, store_id: str, db: Session = Depends(get_db)):
    store = db.query(Store).filter(Store.id == store_id).first()
    if not store:
        raise HTTPException(status_code=404, detail="Tienda no encontrada")
    store.is_active = False
    db.commit()