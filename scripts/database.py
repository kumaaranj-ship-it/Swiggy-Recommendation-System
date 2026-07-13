import sqlite3
from pathlib import Path

# =====================================================
# PROJECT PATHS
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_DIR = BASE_DIR / "database"

DATABASE_PATH = DATABASE_DIR / "swiggy.db"

# =====================================================
# CREATE DATABASE DIRECTORY
# =====================================================

DATABASE_DIR.mkdir(
    parents=True,
    exist_ok=True
)

# =====================================================
# CREATE DATABASE CONNECTION
# =====================================================

connection = sqlite3.connect(DATABASE_PATH)

cursor = connection.cursor()

print("=" * 60)
print("Swiggy Recommendation System Database")
print("=" * 60)
print(f"Database Location : {DATABASE_PATH}")
print()
# =====================================================
# RESTAURANTS TABLE
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS restaurants (

    restaurant_id INTEGER PRIMARY KEY,

    name TEXT NOT NULL,

    city TEXT NOT NULL,

    cuisine TEXT NOT NULL,

    rating REAL,

    rating_count INTEGER,

    cost REAL,

    address TEXT

)
""")

print("✓ restaurants table created")


# =====================================================
# USERS TABLE
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (

    user_id INTEGER PRIMARY KEY AUTOINCREMENT,

    username TEXT NOT NULL UNIQUE,

    email TEXT NOT NULL UNIQUE,

    password TEXT NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)
""")

print("✓ users table created")

cursor.execute("DROP TABLE IF EXISTS search_history")
cursor.execute("DROP TABLE IF EXISTS click_history")
cursor.execute("DROP TABLE IF EXISTS favourites")
cursor.execute("DROP TABLE IF EXISTS ratings")
cursor.execute("DROP TABLE IF EXISTS user_preferences")

# =====================================================
# SEARCH HISTORY TABLE
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS search_history (

    search_id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id INTEGER NOT NULL,

    search_query TEXT NOT NULL,

    search_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)
        REFERENCES users(user_id)

)
""")

print("✓ search_history table created")


# =====================================================
# CLICK HISTORY TABLE
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS click_history (

    click_id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id INTEGER NOT NULL,

    restaurant_id INTEGER NOT NULL,

    click_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)
        REFERENCES users(user_id),

    FOREIGN KEY (restaurant_id)
        REFERENCES restaurants(restaurant_id)

)
""")

print("✓ click_history table created")


# =====================================================
# FAVOURITES TABLE
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS favourites (

    favourite_id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id INTEGER NOT NULL,

    restaurant_id INTEGER NOT NULL,

    added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)
        REFERENCES users(user_id),

    FOREIGN KEY (restaurant_id)
        REFERENCES restaurants(restaurant_id)

)
""")

print("✓ favourites table created")


# =====================================================
# RATINGS TABLE
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS ratings (

    rating_id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id INTEGER NOT NULL,

    restaurant_id INTEGER NOT NULL,

    rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),

    rating_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)
        REFERENCES users(user_id),

    FOREIGN KEY (restaurant_id)
        REFERENCES restaurants(restaurant_id)

)
""")

print("✓ ratings table created")
## ==========================================
# User Preferences Table
# ==========================================

# Create new table
cursor.execute("""
CREATE TABLE IF NOT EXISTS user_preferences (

    preference_id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id INTEGER NOT NULL,

    preference_type TEXT NOT NULL,

    preference_value TEXT NOT NULL,

    score REAL NOT NULL,

    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)
        REFERENCES users(user_id)
)
""")

print("✓ user_preferences table created")
# =====================================================
# SAVE ALL CHANGES
# =====================================================

connection.commit()

print()
print("Database schema created successfully.")

# =====================================================
# VERIFY DATABASE TABLES
# =====================================================

cursor.execute("""
SELECT name
FROM sqlite_master
WHERE type='table'
ORDER BY name;
""")

tables = cursor.fetchall()

print()
print("=" * 60)
print("AVAILABLE TABLES")
print("=" * 60)

for table in tables:

    print(f"✓ {table[0]}")

# =====================================================
# CLOSE CONNECTION
# =====================================================

connection.close()

print()
print("Database connection closed successfully.")

# =====================================================
# REUSABLE DATABASE FUNCTIONS
# =====================================================

def get_connection():
    """
    Return a new SQLite database connection.
    """

    return sqlite3.connect(DATABASE_PATH)


def get_cursor():
    """
    Return both the database connection
    and cursor.
    """

    connection = get_connection()

    cursor = connection.cursor()

    return connection, cursor


def get_database_path():
    """
    Return the database path.
    """

    return DATABASE_PATH


# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":

    print()
    print("=" * 60)
    print("Database initialization completed successfully.")
    print("=" * 60)
    
    import sqlite3

conn = sqlite3.connect("database/swiggy.db")
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(users)")

for column in cursor.fetchall():
    print(column)

conn.close()