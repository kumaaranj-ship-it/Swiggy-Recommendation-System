from pathlib import Path

import pandas as pd

from scripts.database import get_connection


# =========================================
# FILE PATHS
# =========================================

BASE_DIR = Path(__file__).resolve().parent.parent

CLEANED_DATA_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "cleaned_data.csv"
)


# =========================================
# LOAD CLEANED DATASET
# =========================================

print("\nLoading cleaned dataset...")

df = pd.read_csv(CLEANED_DATA_PATH)

print("Dataset loaded successfully.")

print(f"Restaurants Found : {len(df):,}")


# =========================================
# VALIDATE REQUIRED COLUMNS
# =========================================

required_columns = [
    "id",
    "name",
    "city",
    "cuisine",
    "rating",
    "rating_count",
    "cost",
    "address"
]

missing_columns = [
    col
    for col in required_columns
    if col not in df.columns
]

if missing_columns:

    raise ValueError(
        f"Missing Columns : {missing_columns}"
    )

print("Column validation successful.")


# =========================================
# CONNECT DATABASE
# =========================================

connection = get_connection()

cursor = connection.cursor()

print("Connected to SQLite.")


# =========================================
# CLEAR EXISTING DATA
# =========================================

cursor.execute(
    """
    DELETE FROM restaurants
    """
)

connection.commit()

print("Existing restaurant data cleared.")


# =========================================
# INSERT RESTAURANTS
# =========================================

print("\nLoading restaurants into database...")

cursor.executemany(
    """
    INSERT INTO restaurants
    (
        restaurant_id,
        name,
        city,
        cuisine,
        rating,
        rating_count,
        cost,
        address
    )
    VALUES
    (
        ?,?,?,?,?,?,?,?
    )
    """,
    df[
        [
            "id",
            "name",
            "city",
            "cuisine",
            "rating",
            "rating_count",
            "cost",
            "address"
        ]
    ].values.tolist()
)

connection.commit()

print("Restaurant data inserted successfully.")


# =========================================
# VERIFY INSERTION
# =========================================

cursor.execute(
    """
    SELECT COUNT(*)
    FROM restaurants
    """
)

restaurant_count = cursor.fetchone()[0]

print(f"\nRestaurants in Database : {restaurant_count:,}")


# =========================================
# SAMPLE RECORDS
# =========================================

cursor.execute(
    """
    SELECT
        restaurant_id,
        name,
        city,
        cuisine,
        rating,
        cost
    FROM restaurants
    LIMIT 5
    """
)

sample_data = cursor.fetchall()

print("\nSample Records\n")

for row in sample_data:

    print(row)


# =========================================
# CLOSE CONNECTION
# =========================================

connection.close()

print("\nDatabase connection closed.")