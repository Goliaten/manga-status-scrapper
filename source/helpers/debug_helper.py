from typing import Callable


def log_debug_wrapper(fnc: Callable):
    def wrapper(*args, **kwargs):
        print(f"Entering {fnc.__name__}")
        result = fnc(*args, **kwargs)
        print(f"Exiting {fnc.__name__}")
        return result

    return wrapper


DB_CREATION_SQL = """
-- Disable foreign key constraints for bulk operations (optional, but good practice for setup)
-- PRAGMA foreign_keys = OFF;

-- Table: Roles
CREATE TABLE IF NOT EXISTS Roles (
    role_id INTEGER PRIMARY KEY AUTOINCREMENT,
    role_name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT
);

-- Table: Users
CREATE TABLE IF NOT EXISTS Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT 1, -- 1 for active, 0 for inactive
    FOREIGN KEY (role_id) REFERENCES Roles (role_id)
);

-- Table: Permissions
CREATE TABLE IF NOT EXISTS Permissions (
    permission_id INTEGER PRIMARY KEY AUTOINCREMENT,
    permission_name VARCHAR(100) UNIQUE NOT NULL
);

-- Table: Role_Permissions (Junction table)
CREATE TABLE IF NOT EXISTS Role_Permissions (
    role_id INTEGER NOT NULL,
    permission_id INTEGER NOT NULL,
    PRIMARY KEY (role_id, permission_id),
    FOREIGN KEY (role_id) REFERENCES Roles (role_id),
    FOREIGN KEY (permission_id) REFERENCES Permissions (permission_id)
);

-- Table: Scraping_Scripts
CREATE TABLE IF NOT EXISTS Scraping_Scripts (
    script_id INTEGER PRIMARY KEY AUTOINCREMENT,
    script_name VARCHAR(255) UNIQUE NOT NULL,
    script_path VARCHAR(500) NOT NULL,
    last_modified_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    description TEXT
);

-- Table: Comics
CREATE TABLE IF NOT EXISTS Comics (
    comic_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(255) UNIQUE NOT NULL,
    alternative_titles TEXT, -- Stored as JSON string
    description TEXT,
    author VARCHAR(255),
    artist VARCHAR(255),
    genre VARCHAR(255),
    status VARCHAR(50),
    cover_image_url VARCHAR(500),
    is_scraping_enabled BOOLEAN DEFAULT 1, -- 1 for enabled, 0 for disabled
    scraping_script_id INTEGER,
    source_url VARCHAR(500),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (scraping_script_id) REFERENCES Scraping_Scripts (script_id)
);

-- Table: Scraping_History
CREATE TABLE IF NOT EXISTS Scraping_History (
    history_id INTEGER PRIMARY KEY AUTOINCREMENT,
    comic_id INTEGER NOT NULL,
    chapter_number DECIMAL(10, 2) NOT NULL,
    chapter_title VARCHAR(500),
    scraped_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    url VARCHAR(500),
    FOREIGN KEY (comic_id) REFERENCES Comics (comic_id)
);

-- Table: User_Subscriptions (Junction table)
CREATE TABLE IF NOT EXISTS User_Subscriptions (
    user_id INTEGER NOT NULL,
    comic_id INTEGER NOT NULL,
    subscribed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, comic_id),
    FOREIGN KEY (user_id) REFERENCES Users (user_id),
    FOREIGN KEY (comic_id) REFERENCES Comics (comic_id)
);

-- Re-enable foreign key constraints if you disabled them earlier
-- PRAGMA foreign_keys = ON;
"""
