from pathlib import Path

RUNTIME_PATH = "."
"""Points to root of the project.
Change this if you want to be able to execute this script from different location than root dir.
"""

PARAMS_FILENAME = "params.toml"
PARAMS_PATH = str(Path(RUNTIME_PATH, PARAMS_FILENAME))

LOG_DIR = "logs"
DATABASE_DIR = "database"
DATABASE_NAME = "base.db"
DATABASE_PATH = str(Path(DATABASE_DIR, DATABASE_NAME))
