from datetime import datetime
from pathlib import Path
from typing import List
import sqlite3

import source.config as cfg
from source.data_classes import ScrapingHistory, ScrapingScript, ScrapingInstance
from source.DB.BaseDBManager import BaseDBManager


class SQLiteManager(BaseDBManager):
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
        print("getting scraping instances")
        sql = """
            SELECT
                *
            FROM
                T_SCRAPING_INSTANCE
            """
        if kwarg:
            sql += self.__condition_adder(**kwarg)

        db_data = self.execute(sql).fetchall()
        try:
            instances = [ScrapingInstance(*x) for x in db_data]
        except Exception as e:
            print(db_data)
            import traceback

            traceback.print_exc()
            exit(1)
        return instances

    def get_scraping_scripts(self, **kwarg) -> List[ScrapingScript]:
        print("getting scraping scripts")
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
        print("getting scraping script")
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

    def insert_scraping_history(
        self, scraping_history: List[ScrapingHistory]
    ) -> List[int]:
        print("inserting scraping history")
        if not scraping_history:
            # TODO log that nothing happened
            return []
        out_id = []
        self.db.execute("begin")
        for scrap_hist in scraping_history:
            keys = [x[0] for x in scrap_hist.__dict__.items() if x[1]]
            values = [
                x[1].strftime(cfg.DATETIME_FORMAT)
                if isinstance(x, datetime)
                else str(x[1])
                for x in scrap_hist.__dict__.items()
                if x[1]
            ]

            sql = f"""
                INSERT INTO 
                    T_SCRAPING_HISTORY
                    ({", ".join(keys)})
                VALUES
                    ({", ".join(values)})"""
            x = self.execute(sql)
            if not x.rowcount or not x.lastrowid:
                print(f"could not insert scraping history {scrap_hist=}")
                self.db.execute("rollback")
                return []

            out_id.append(x.lastrowid)

        # x.connection.commit()
        self.db.execute("commit")
        print(f" updated {len(out_id)} rows")

        return out_id
