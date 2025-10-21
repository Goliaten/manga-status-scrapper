from typing import Any, List

from source.DB import BaseDBManager
from source.data_classes import ScrapingHistory, ScrapingInstance
from .BasicScrapper import BasicScrapper


class TestScrapper(BasicScrapper):
    def scrape(self, url: str) -> Any:
        print(f"Dummy test scrape for {url=}")
        return "Test return"

    def upsert_data(
        self, db_manager: BaseDBManager, scraping_instance: ScrapingInstance, data: Any
    ):
        new_history = ScrapingHistory(None, scraping_instance.id, -1, None, None)
        db_manager.insert_scraping_history([new_history, new_history])
