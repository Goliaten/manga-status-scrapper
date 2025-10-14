from abc import abstractmethod
from typing import Any, Dict, List, Tuple
from source.dataclasses.ScrapResult import ScrapResult


class BaseDBManager:
    @abstractmethod
    def insert_scrap_results(
        self, scrap_results: List[ScrapResult]
    ) -> Tuple[int, str]: ...

    @abstractmethod
    def get_scrap_results(self, filters: Dict[str, Any]) -> List[ScrapResult]: ...

    @abstractmethod
    def upsert_scrap_results(
        self, scrap_results: List[ScrapResult]
    ) -> Tuple[int, str]: ...

    @abstractmethod
    def deactivate_scrap_results(self, filters: Dict[str, Any]) -> Tuple[int, str]: ...
