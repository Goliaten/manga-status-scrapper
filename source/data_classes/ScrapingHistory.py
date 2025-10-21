from dataclasses import dataclass
from datetime import datetime
from typing import Optional

# from source.data_classes.BaseDataclass import BaseDataclass
import source.config as cfg


@dataclass
class ScrapingHistory:
    id: Optional[int]  # if id exists, it's row from DB. Else it's new row
    scraping_instance_id: int
    chapter_number: float
    chapter_title: Optional[str]
    scraped_at: Optional[datetime]

    def __post_init__(self):
        if self.scraped_at:
            self.scraped_at = datetime.strptime(self.scraped_at, cfg.DATETIME_FORMAT)
