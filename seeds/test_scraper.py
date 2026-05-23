import asyncio
from app.scrapers.thomann import ThomannScraper

async def main():
    scraper = ThomannScraper()
    url     = "https://www.thomann.es/larry_carlton_l7_bk_new_gen.htm"
    result  = await scraper.scrape(url)
    print(f"Precio:   {result.price} {result.currency}")
    print(f"En stock: {result.in_stock}")
    print(f"Estado:   {result.status}")

asyncio.run(main())