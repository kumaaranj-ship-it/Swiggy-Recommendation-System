import pandas as pd
import os
import joblib

from sklearn.preprocessing import OneHotEncoder


# =========================================
# FILE PATHS
# =========================================

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

CLEANED_DATA_PATH = BASE_DIR / "data" / "processed" / "cleaned_data.csv"
ENCODED_DATA_PATH = BASE_DIR / "data" / "processed" / "encoded_data.csv"
ENCODER_PATH = BASE_DIR / "models" / "encoder.pkl"


# =========================================
# LOAD CLEANED DATASET
# =========================================

print("\nLoading cleaned dataset...")

df = pd.read_csv(CLEANED_DATA_PATH)

print("Dataset loaded successfully.")

print("\nDataset Shape:")
print(df.shape)

required_columns = [
    "city",
    "cuisine",
    "rating",
    "rating_count",
    "cost"
]

missing_columns = [
    col
    for col in required_columns
    if col not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Missing required columns: {missing_columns}"
    )

# =========================================
# SELECT FEATURES
# =========================================

categorical_features = [
    'city',
    'cuisine'
]

numerical_features = [
    'rating',
    'rating_count',
    'cost'
]

print("\nSelected categorical and numerical features.")


# =========================================
# HANDLE MISSING VALUES
# =========================================

for col in categorical_features:
    df[col] = df[col].fillna("Unknown")

for col in numerical_features:
    df[col] = df[col].fillna(0)

print("\nMissing values handled.")


# =========================================
# CREATE ONE-HOT ENCODER
# =========================================

print("\nApplying One-Hot Encoding...")

encoder = OneHotEncoder(
    handle_unknown='ignore',
    sparse_output=True
)


# =========================================
# FIT AND TRANSFORM
# =========================================

encoded_sparse = encoder.fit_transform(df[categorical_features])

print("Encoding completed.")


# =========================================
# GET FEATURE NAMES
# =========================================

encoded_feature_names = encoder.get_feature_names_out(
    categorical_features
)


# =========================================
# CONVERT TO DATAFRAME
# =========================================

encoded_df = pd.DataFrame.sparse.from_spmatrix(
    encoded_sparse,
    columns=encoded_feature_names,
    index=df.index
)

# Preserve original mapping
encoded_df.insert(
    0,
    "original_index",
    df.index
)

# If the cleaned dataset contains an 'id' column,
# preserve it as well for safer mapping.
if "id" in df.columns:
    encoded_df.insert(
        1,
        "restaurant_id",
        df["id"].values
    )

print("\nEncoded DataFrame created.")


# =========================================
# COMBINE ENCODED + NUMERICAL FEATURES
# =========================================

final_df = pd.concat(
    [encoded_df, df[numerical_features]],
    axis=1
)

print("\nFinal encoded dataset created.")

# =========================================
# VALIDATION CHECKS
# =========================================

print("\nRunning validation checks...")

# Check row alignment
assert len(final_df) == len(df), \
    "Row count mismatch between cleaned and encoded datasets."

# Check for missing values
assert final_df.isnull().sum().sum() == 0, \
    "Encoded dataset contains missing values."

# Ensure every column is numeric
non_numeric_cols = final_df.select_dtypes(exclude=["number"]).columns.tolist()

assert len(non_numeric_cols) == 0, \
    f"Non-numeric columns found: {non_numeric_cols}"

print("All validation checks passed.")


# =========================================
# FINAL DATASET INFO
# =========================================

print("\nEncoded Dataset Shape:")
print(final_df.shape)

print("\nFirst 5 Rows:")
print(final_df.head())


# =========================================
# CREATE OUTPUT DIRECTORIES
# =========================================

os.makedirs("data/processed", exist_ok=True)

os.makedirs("models", exist_ok=True)


# =========================================
# SAVE ENCODED DATASET
# =========================================

final_df.to_csv(
    ENCODED_DATA_PATH,
    index=False
)

print(f"\nEncoded dataset saved to:\n{ENCODED_DATA_PATH}")


# =========================================
# SAVE ENCODER
# =========================================

joblib.dump(
    encoder,
    ENCODER_PATH
)

print("\nEncoder Categories:")

for feature, categories in zip(
    categorical_features,
    encoder.categories_
):
    print(f"{feature}: {len(categories)} categories")