from datetime import datetime
from typing import Literal, Tuple
from .BasicScrapper import BasicScrapper
import bs4

from source.data_classes import ScrapingHistory, ScrapingInstance
from source.DB import BaseDBManager
from source.helpers.ScrapperHelpers import get_html_from_url


class ManhuasScrapper(BasicScrapper):
    """
    Scrapper designed for `manhuas.com` website.
    """

    def scrape(
        self, url: str
    ) -> (
        Tuple[Literal[False], None, float | None, str | None, str | None]
        | Tuple[Literal[True], str, None, None, None]
    ):
        """
        Returns
        --------
        Tuple
            4 element tuple containing the following:
            - error flag - if 1 then error, if 0 then no error
            - error msg
            - chapter number
            - chapter title
            - chapter added date
        """

        raw_html = get_html_from_url(url)
        if raw_html[1]:
            return (True, f"Request error: {raw_html[2]}", None, None, None)

        soup = bs4.BeautifulSoup(raw_html[0], "lxml")

        items = soup.find_all("li", {"class": "wp-manga-chapter"})

        if items[0].a:
            chapter_title: str | None = items[0].a.text
            if chapter_title:
                chapter_title = chapter_title.strip()

            try:
                if not chapter_title:
                    raise ValueError
                chapter_num = float(chapter_title.split(" ")[-1])
            except:  # noqa: E722
                chapter_num = None
        else:
            chapter_title = None
            chapter_num = None

        if items[0].span:
            chapter_date: str | None = items[0].span.text
            if chapter_date:
                chapter_date = chapter_date.strip()
        else:
            chapter_date = None

        return (False, None, chapter_num, chapter_title, chapter_date)

    def upsert_data(
        self,
        db_manager: BaseDBManager,
        scraping_instance: ScrapingInstance,
        data: Tuple[Literal[False], None, float | None, str | None, str | None]
        | Tuple[Literal[True], str, None, None, None],
    ):
        if not data[0] and data[2]:
            sc = ScrapingHistory(
                None,
                scraping_instance.id,
                data[2],
                data[3],
                datetime.now(),
            )
            db_manager.insert_scraping_history([sc])
        else:
            print("Invalid scraping.")
