import re
from playwright.async_api import async_playwright
from app.scrapers.base import BaseScraper, ScrapeResult

class ThomannScraper(BaseScraper):

    async def scrape(self, url: str) -> ScrapeResult:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page    = await browser.new_page()

            try:
                # Cabeceras para parecer un navegador real
                await page.set_extra_http_headers({
                    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
                    "Accept-Language": "es-ES,es;q=0.9"
                })

                await page.goto(url, wait_until="domcontentloaded", timeout=30000)

                # Espera a que el precio esté visible
                await page.wait_for_selector(".price", timeout=10000)

                # Extrae el texto del precio
                price_text = await page.inner_text(".price")

                # Limpia el texto: "499,00 €" → 499.00
                price = self._parse_price(price_text)

                # Comprueba si está en stock
                in_stock = await self._check_stock(page)

                return ScrapeResult(price=price, currency="EUR", in_stock=in_stock)

            except Exception as e:
                return ScrapeResult(price=0, currency="EUR", in_stock=False, status="error")

            finally:
                await browser.close()

    def _parse_price(self, text: str) -> float:
        # Elimina todo excepto números, comas y puntos
        cleaned = re.sub(r'[^\d,.]', '', text)
        # Convierte formato europeo "499,00" a float 499.0
        cleaned = cleaned.replace('.', '').replace(',', '.')
        return float(cleaned)

    async def _check_stock(self, page) -> bool:
        try:
            # Thomann suele tener un botón de añadir al carrito si hay stock
            add_button = await page.query_selector(".addToBasket")
            return add_button is not None
        except:
            return True  # asume en stock si no puede determinarlo