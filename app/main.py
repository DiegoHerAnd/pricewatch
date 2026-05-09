from fastapi import FastAPI
from app.routers import products, categories, stores
from scalar_fastapi import get_scalar_api_reference
app = FastAPI(
    title="PriceWatch API",
    version="1.0.0",
    docs_url=None,
    redoc_url=None
)

@app.get("/docs", include_in_schema=False)
def scalar_docs():
    return get_scalar_api_reference(
        openapi_url="/openapi.json",
        title="PriceWatch API"
    )
app.include_router(products.router,   prefix="/api/v1")
app.include_router(categories.router, prefix="/api/v1")
app.include_router(stores.router,     prefix="/api/v1")