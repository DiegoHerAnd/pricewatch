from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from app.models.category import Category
from app.core.limiter import limiter

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.get("/",
            response_model=list[CategoryResponse],
            summary = "Listar Categorias",
            description = "Devuelve todas las categorias activas registradas en el sistema."
            )
@limiter.limit("30/minute")
def get_categories(request: Request, db: Session = Depends(get_db)):
    return db.query(Category).all()

@router.get("/{category_id}",
            response_model=CategoryResponse,
            summary = "Obtener categorias",
            description = "Devuelve el detalle de una categoria en concreto por su ID."
            )
@limiter.limit("30/minute")
def get_category(request: Request, category_id: str, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return category

@router.post("/",
             response_model=CategoryResponse,
             status_code=201,
             summary = "Crear categoria",
             description = "Crea una nueva categoría."
             )
@limiter.limit("10/minute")
def create_category(request: Request, data: CategoryCreate, db: Session = Depends(get_db)):
    category = Category(**data.model_dump())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

@router.put("/{category_id}",
            response_model=CategoryResponse,
            summary = "Actualizar categoria",
            description = "Actualiza los campos de una categoría existente. Solo se modifican los campos enviados."
            )
@limiter.limit("10/minute")
def update_category(request: Request, category_id: str, data: CategoryUpdate, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(category, key, value)
    db.commit()
    db.refresh(category)
    return category

@router.delete("/{category_id}",
               status_code=204,
               summary ="Eliminar categoría",
               description= "Desactiva una categoria (soft delete). No se borra físicamente de la base de datos."
               )
@limiter.limit("5/minute")
def delete_category(request: Request, category_id: str, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    db.delete(category)
    db.commit()