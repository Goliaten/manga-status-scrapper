from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional

# from source.data_classes.BaseDataclass import BaseDataclass
import source.config as cfg


@dataclass
class ScrapingInstance:
    id: int
    created_at: Optional[datetime]
    last_updated_at: Optional[datetime]
    is_active: Optional[bool]
    scraping_url: str
    scraping_interval: int
    last_scrap_at: Optional[datetime]
    comic_id: int
    scraping_script_id: int

    def __post_init__(self):
        self.created_at = datetime.strptime(self.created_at, cfg.DATETIME_FORMAT)
        self.last_updated_at = datetime.strptime(
            self.last_updated_at, cfg.DATETIME_FORMAT
        )
        if self.last_scrap_at:
            self.last_scrap_at = datetime.strptime(
                self.last_scrap_at, cfg.DATETIME_FORMAT
            )

    def is_scraping_due(self) -> bool:
        """
        Check whether instance should be scrapped.
        """
        if not self.last_scrap_at:
            return True
        if (
            self.last_scrap_at + timedelta(seconds=self.scraping_interval)
            <= datetime.now()
        ):
            return True
        return False
