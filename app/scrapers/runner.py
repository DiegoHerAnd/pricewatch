import asyncio
from app.core.database import SessionLocal
from app.models.product_store_url import ProductStoreUrl
from app.models.price_history import PriceHistory
from app.scrapers.thomann import ThomannScraper

SCRAPERS = {
    "Thomann": ThomannScraper(),
}

async def run_scraper_for_url(psu: ProductStoreUrl, db):
    scraper = SCRAPERS.get(psu.store.name)
    if not scraper:
        print(f"No hay scraper para {psu.store.name}")
        return

    result = await scraper.scrape(psu.url)

    entry = PriceHistory(
        product_store_url_id=psu.id,
        price=result.price,
        currency=result.currency,
        in_stock=result.in_stock,
        scraped_status=result.status
    )
    db.add(entry)
    db.commit()
    print(f"✅ {psu.product.name} — {result.price}€ ({result.status})")

async def run_all():
    db  = SessionLocal()
    urls = db.query(ProductStoreUrl).filter(ProductStoreUrl.is_active == True).all()
    for psu in urls:
        await run_scraper_for_url(psu, db)
    db.close()

if __name__ == "__main__":
    asyncio.run(run_all())