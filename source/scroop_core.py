from typing import Any, List
import time
import logging
from source.DB.SQLiteManager import SQLiteManager
from source.data_classes import ScrapingInstance
import source.scrapping_classes as sc


def check_db_integrity():
    print("checking db integrity")
    # TODO check if all tables are there
    # TODO check if table structure matches dataclasses
    pass


def get_scraping_instances() -> List[ScrapingInstance]:
    print("getting scraping instances from db")
    # TODO get scraping instances from db
    instances = SQLiteManager().get_scraping_instances()
    # TODO check if it's time to scrape them
    instances = [x for x in instances if x.is_scraping_due()]
    return instances


def scrape(instances: List[ScrapingInstance]) -> Any:
    # TODO maybe add option to also scan the content of the website for other comics
    print("scraping")
    # loop over the instances
    for instance in instances:
        script = SQLiteManager().get_scraping_script(id=instance.scraping_script_id)

        if script.class_name in sc.__dict__:
            print(f"{script.class_name=}")
            scraper: sc.BasicScrapper = sc.__dict__[script.class_name]()
            # scrape
            scraper.scrape(instance.scraping_url)
            # TODO put status in scraping history
        else:
            raise ValueError("Invalid scraping class")  # for now i'll raise an error
            # TODO put scraping error in history
            # TODO write error to logs
        exit("aaa")
    pass


def core():
    # TODO make proper logger
    SLEEP_TIME = 60
    print("starting core")
    check_db_integrity()

    while True:
        instances = get_scraping_instances()
        print(instances)

        scrape(instances)

        time.sleep(SLEEP_TIME)

    # check if there is something to scrap
    # if yes, scrap everything, and insert it to database
    pass


if __name__ == "__main__":
    # SQLiteManager().init_db()
    core()
