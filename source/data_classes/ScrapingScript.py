from dataclasses import dataclass
from datetime import datetime
from typing import Optional

# from source.data_classes.BaseDataclass import BaseDataclass
import source.config as cfg


@dataclass
class ScrapingScript:
    id: int
    created_at: Optional[datetime]
    last_updated_at: Optional[datetime]
    class_name: str

    def __post_init__(self):
        self.created_at = datetime.strptime(self.created_at, cfg.DATETIME_FORMAT)
        self.last_updated_at = datetime.strptime(
            self.last_updated_at, cfg.DATETIME_FORMAT
        )
