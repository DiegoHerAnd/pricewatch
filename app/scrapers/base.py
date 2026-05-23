from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class ScrapeResult:
    price:    float
    currency: str
    in_stock: bool
    status:   str = "success"  # 'success' | 'error' | 'blocked'

class BaseScraper(ABC):

    @abstractmethod
    async def scrape(self, url: str) -> ScrapeResult:
        """Raspa el precio de una URL y devuelve un ScrapeResult."""
        pass