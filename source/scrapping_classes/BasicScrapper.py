from abc import ABC, abstractmethod
from typing import Any


class BasicScrapper(ABC):
    @abstractmethod
    def scrape(self, url: str) -> Any:
        raise NotImplementedError
