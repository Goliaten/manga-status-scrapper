from abc import ABC, abstractmethod
from typing import List

from source.data_classes import ScrapingHistory, ScrapingInstance, ScrapingScript
from source.helpers.Singleton import Singleton
# from .data_classes.ScrapResult import ScrapResult


class BaseDBManager(ABC, Singleton):
    @abstractmethod
    def get_scraping_instances(self, **kwarg) -> List[ScrapingInstance]:
        raise NotImplementedError

    @abstractmethod
    def get_scraping_scripts(self, **kwarg) -> List[ScrapingScript]:
        raise NotImplementedError

    @abstractmethod
    def get_scraping_script(self, **kwarg) -> ScrapingScript:
        raise NotImplementedError

    @abstractmethod
    def insert_scraping_history(
        self, scraping_history: List[ScrapingHistory]
    ) -> List[int]:
        raise NotImplementedError

    @abstractmethod
    def update_instance(self, scraping_instance: ScrapingInstance) -> None:
        raise NotImplementedError
