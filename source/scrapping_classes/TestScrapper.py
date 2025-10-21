from typing import Any
from .BasicScrapper import BasicScrapper


class TestScrapper(BasicScrapper):
    def scrape(self, url: str) -> Any:
        print(f"Dummy test scrape for {url=}")
        return "Test return"
