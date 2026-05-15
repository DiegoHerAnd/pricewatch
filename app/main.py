from fastapi import FastAPI
from app.routers import products, categories, stores
from scalar_fastapi import get_scalar_api_reference
from app.core.limiter import limiter
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.core.limiter import limiter
from app.routers import products, categories, stores

description = """
PriceWatch te permite registrar productos de cualquier categoría y hacer seguimiento
de su evolución de precios en múltiples tiendas y plataformas.

## Recursos principales

- **Products** — gestión de productos y consulta de historial de precios
- **Categories** — categorías jerárquicas para organizar productos
- **Stores** — tiendas y plataformas donde se monitorizan los precios
"""

app = FastAPI(
    title="PriceWatch API",
    version="1.0.0",
    description=description,
    contact={
        "name": "Diego",
        "url": "https://github.com/DiegoHerAnd/pricewatch",
    },
    license_info={
        "name": "MIT",
    },

    docs_url=None,
    redoc_url=None
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(products.router,   prefix="/api/v1")
app.include_router(categories.router, prefix="/api/v1")
app.include_router(stores.router,     prefix="/api/v1")

@app.get("/docs", include_in_schema=False)
def scalar_docs():
    return get_scalar_api_reference(
        openapi_url="/openapi.json",
        title="PriceWatch API"
    )