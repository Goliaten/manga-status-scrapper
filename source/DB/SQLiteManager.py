from pathlib import Path
from typing import List
import sqlite3

import source.config as cfg
from source.data_classes import ScrapingScript, ScrapingInstance
from source.helpers.Singleton import Singleton
from source.DB.BaseDBManager import BaseDBManager


class SQLiteManager(BaseDBManager, Singleton):
    def __init__(self):
        db_exists = Path(cfg.DATABASE_PATH).exists()
        if not db_exists:
            Path(cfg.DATABASE_PATH).parent.mkdir(exist_ok=True)
        self.db = sqlite3.connect(cfg.DATABASE_PATH)
        self.cursor = self.db.cursor()
        if not db_exists:
            self.init_db()

    @staticmethod
    def __condition_adder(**kwarg) -> str:
        sql = ""

        sql += "\nWHERE "
        for cnt, (key, value) in enumerate(kwarg.items()):
            if cnt != 0:
                sql += "AND "
            sql += f"{key} = {value}"

        return sql

    def execute(self, sql: str) -> sqlite3.Cursor:
        return self.cursor.execute(sql)

    def init_db(self):
        with open("db.sql", "r") as file:
            sql = file.read()
            self.cursor.executescript(sql)

    def get_scraping_instances(self, **kwarg) -> List[ScrapingInstance]:
        sql = """
            SELECT
                *
            FROM
                T_SCRAPING_INSTANCE
            """
        if kwarg:
            sql += self.__condition_adder(**kwarg)

        instances = [ScrapingInstance(*x) for x in self.execute(sql).fetchall()]
        return instances

    def get_scraping_scripts(self, **kwarg) -> List[ScrapingScript]:
        sql = """
            SELECT
                *
            FROM
                T_SCRAPING_SCRIPT
            """
        if kwarg:
            sql += self.__condition_adder(**kwarg)

        scripts = [ScrapingScript(*x) for x in self.execute(sql).fetchall()]
        return scripts

    def get_scraping_script(self, **kwarg) -> ScrapingScript:
        sql = """
            SELECT
                *
            FROM
                T_SCRAPING_SCRIPT
            """
        if kwarg:
            sql += self.__condition_adder(**kwarg)
        sql += "\nlimit 1"

        x = self.execute(sql).fetchone()
        script = ScrapingScript(*x)
        return script
