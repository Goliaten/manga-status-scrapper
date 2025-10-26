from abc import ABC, abstractmethod
from typing import Any

from source.DB import BaseDBManager
from source.data_classes import ScrapingInstance


class BasicScrapper(ABC):
    @abstractmethod
    def scrape(self, url: str) -> Any:
        raise NotImplementedError

    @abstractmethod
    def upsert_data(
        self, db_manager: BaseDBManager, scraping_instance: ScrapingInstance, data: Any
    ) -> Any:
        raise NotImplementedError
