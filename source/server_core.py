import os
import sqlite3

from flask import Flask

from source import API_routes

if __name__ == "__main__":
    import config as cfg  # type: ignore

else:
    import source.config as cfg


def check_if_db_exists(create=True):
    if os.path.exists(cfg.DATABASE_PATH):
        return
    elif not create:
        raise FileNotFoundError("Database is missing")

    cfg.DATABASE_DIR.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(str(cfg.DATABASE_PATH)):
        pass
    # cfg.DATABASE_PATH.touch()


def check_db_structure(cur: sqlite3.Cursor, ammend=True):
    print(f"TODO {__name__}")


def check_db():
    # check if database exists
    check_if_db_exists()

    # check if database structure is appropriate
    with sqlite3.connect(str(cfg.DATABASE_PATH)) as con:
        cur = con.cursor()
        check_db_structure(cur)


# check_db()
# start the web server API
app = Flask(cfg.FLASK_APP_NAME)

app.register_blueprint(API_routes.routes)
