from abc import ABC, abstractmethod
from typing import Any, Dict, List, Tuple

from source.data_classes import ScrapingInstance, ScrapingScript
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
