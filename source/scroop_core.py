from datetime import datetime
from typing import Any, List
import time
from source.DB import BaseDBManager
from source.DB.SQLiteManager import SQLiteManager
from source.data_classes import ScrapingInstance
import source.scrapping_classes as sc


def check_db_integrity(db_manager: BaseDBManager):
    print("checking db integrity")
    # TODO check if all tables are there
    # TODO check if table structure matches dataclasses
    pass


def get_scraping_instances(db_manager: BaseDBManager) -> List[ScrapingInstance]:
    print("getting scraping instances from db")
    # TODO get scraping instances from db
    instances = db_manager.get_scraping_instances()
    # TODO check if it's time to scrape them
    instances = [x for x in instances if x.is_scraping_due()]
    return instances


def scrape(db_manager: BaseDBManager, instances: List[ScrapingInstance]) -> Any:
    # TODO maybe add option to also scan the content of the website for other comics
    print(f"scraping {len(instances)} instances")
    # loop over the instances
    for instance in instances:
        script = db_manager.get_scraping_script(id=instance.scraping_script_id)

        if script.class_name not in sc.__dict__:
            print(
                f"Scraping class not found. Received '{script.class_name}', got '{sc.__dict__}'."
            )
            raise ValueError("Invalid scraping class")  # for now i'll raise an error
            # TODO put scraping error in history
            # TODO write error to logs

        print(f"{script.class_name=}")
        scraper: sc.BasicScrapper = sc.__dict__[script.class_name]()
        # scrape
        scrape_data = scraper.scrape(instance.scraping_url)
        # put status in scraping history
        scraper.upsert_data(db_manager, instance, scrape_data)
        # TODO log scraping status
        # update instance
        instance.last_scrap_at = datetime.now()
        db_manager.update_instance(instance)


def get_db_manager():
    return SQLiteManager()


def core():
    # TODO make proper logger
    print("starting core")
    db_manager = get_db_manager()
    check_db_integrity(db_manager)

    instances = get_scraping_instances(db_manager)

    scrape(db_manager, instances)


if __name__ == "__main__":
    core()
