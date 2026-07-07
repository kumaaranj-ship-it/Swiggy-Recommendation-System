import pandas as pd
import os


# =========================================
# FILE PATHS
# =========================================

RAW_DATA_PATH = "data/raw/swiggy.csv"
CLEANED_DATA_PATH = "data/processed/cleaned_data.csv"


# =========================================
# LOAD DATASET
# =========================================

print("\nLoading Swiggy dataset...")

df = pd.read_csv(RAW_DATA_PATH)

print("Dataset loaded successfully.")


# =========================================
# BASIC DATASET INFORMATION
# =========================================

print("\nDataset Shape:")
print(df.shape)

print("\nColumn Names:")
print(df.columns.tolist())

print("\nFirst 5 Rows:")
print(df.head())

print("\nMissing Values:")
print(df.isnull().sum())


# =========================================
# REMOVE DUPLICATES
# =========================================

initial_rows = df.shape[0]

df = df.drop_duplicates()

final_rows = df.shape[0]

print(f"\nRemoved {initial_rows - final_rows} duplicate rows.")


# =========================================
# SELECT IMPORTANT COLUMNS
# =========================================

required_columns = [
    'id',
    'name',
    'city',
    'rating',
    'rating_count',
    'cost',
    'cuisine',
    'address'
]

df = df[required_columns]

print("\nSelected required columns.")


# =========================================
# CLEAN TEXT COLUMNS
# =========================================

text_columns = ['name', 'city', 'cuisine', 'address']

for col in text_columns:

    # Fill missing values
    df[col] = df[col].fillna("Unknown")

    # Convert to string
    df[col] = df[col].astype(str)

    # Remove extra spaces
    df[col] = df[col].str.strip()

print("\nText columns cleaned.")

# =========================================
# VALIDATE CUISINE COLUMN
# =========================================

print("\nValidating cuisine column...")

# Patterns that indicate the value is NOT a cuisine
invalid_patterns = [
    r"\d{1,2}:\d{2}",     # 8:15
    r"\bAM\b",
    r"\bPM\b",
    r"\bTo\b",
    r"www\.",
    r"http",
]

invalid_mask = df["cuisine"].str.contains(
    "|".join(invalid_patterns),
    case=False,
    regex=True,
    na=False
)

invalid_count = invalid_mask.sum()

df.loc[invalid_mask, "cuisine"] = "Unknown"

print(f"Replaced {invalid_count} invalid cuisine values with 'Unknown'.")

df["cuisine"] = (
    df["cuisine"]
    .str.replace(r"\s+", " ", regex=True)
    .str.title()
)
# =========================================
# CLEAN RATING COLUMN
# =========================================

print("\nCleaning rating column...")

# Convert to string
df['rating'] = df['rating'].astype(str)

# Extract numeric values only
df['rating'] = df['rating'].str.extract(r'(\d+\.?\d*)')

# Convert to numeric
df['rating'] = pd.to_numeric(
    df['rating'],
    errors='coerce'
)

# Fill missing ratings with median
median_rating = df['rating'].median()

df['rating'] = df['rating'].fillna(median_rating)

print("Rating column cleaned.")


# =========================================
# CLEAN RATING COUNT COLUMN
# =========================================

print("\nCleaning rating_count column...")

df['rating_count'] = df['rating_count'].astype(str)

# Remove commas
df['rating_count'] = df['rating_count'].str.replace(',', '')

# Extract numbers
df['rating_count'] = df['rating_count'].str.extract(r'(\d+)')

# Convert to numeric
df['rating_count'] = pd.to_numeric(
    df['rating_count'],
    errors='coerce'
)

# Fill missing values with 0
df['rating_count'] = df['rating_count'].fillna(0)

print("Rating count column cleaned.")


# =========================================
# CLEAN COST COLUMN
# =========================================

print("\nCleaning cost column...")

df['cost'] = df['cost'].astype(str)

# Remove currency symbols and text
df['cost'] = df['cost'].str.replace(
    r'[^\d.]',
    '',
    regex=True
)

# Convert to numeric
df['cost'] = pd.to_numeric(
    df['cost'],
    errors='coerce'
)

# Fill missing values with median cost
median_cost = df['cost'].median()

df['cost'] = df['cost'].fillna(median_cost)

print("Cost column cleaned.")


# =========================================
# FINAL DATASET CHECK
# =========================================

print("\nFinal Dataset Shape:")
print(df.shape)

print("\nRemaining Missing Values:")
print(df.isnull().sum())

print("\nSample Cleaned Data:")
print(df.head())


# =========================================
# CREATE OUTPUT FOLDER
# =========================================

os.makedirs("data/processed", exist_ok=True)


# =========================================
# SAVE CLEANED DATASET
# =========================================

df.to_csv(CLEANED_DATA_PATH, index=False)

print(f"\nCleaned dataset saved to:\n{CLEANED_DATA_PATH}")