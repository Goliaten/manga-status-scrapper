from pathlib import Path

RUNTIME_PATH = "."
"""Points to root of the project.
Change this if you want to be able to execute this script from different location than root dir.
"""

PARAMS_PATH = Path(RUNTIME_PATH, "params.toml")

LOG_DIR = Path(RUNTIME_PATH, "logs")
DATABASE_DIR = Path(RUNTIME_PATH, "database")
DATABASE_PATH = Path(DATABASE_DIR, "base.db")

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"  # YYYY-MM-DD HH:MM:SS

FLASK_APP_NAME = "manga_status"
