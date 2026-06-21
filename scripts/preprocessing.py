import pandas as pd
import os
import joblib

from sklearn.preprocessing import OneHotEncoder


# =========================================
# FILE PATHS
# =========================================

CLEANED_DATA_PATH = "data/processed/cleaned_data.csv"

ENCODED_DATA_PATH = "data/processed/encoded_data.csv"

ENCODER_PATH = "models/encoder.pkl"


# =========================================
# LOAD CLEANED DATASET
# =========================================

print("\nLoading cleaned dataset...")

df = pd.read_csv(CLEANED_DATA_PATH)

print("Dataset loaded successfully.")

print("\nDataset Shape:")
print(df.shape)


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
    sparse_output=False
)


# =========================================
# FIT AND TRANSFORM
# =========================================

encoded_array = encoder.fit_transform(
    df[categorical_features]
)

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

encoded_df = pd.DataFrame(
    encoded_array,
    columns=encoded_feature_names,
    index=df.index
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

print(f"\nEncoder saved to:\n{ENCODER_PATH}")