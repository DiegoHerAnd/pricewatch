from fastapi import FastAPI
from app.routers import products, categories, stores

app = FastAPI(title="PriceWatch API", version="1.0.0")

app.include_router(products.router,   prefix="/api/v1")
app.include_router(categories.router, prefix="/api/v1")
app.include_router(stores.router,     prefix="/api/v1")