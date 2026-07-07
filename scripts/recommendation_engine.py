from pathlib import Path

import joblib
import pandas as pd

from scipy.sparse import csr_matrix
from scipy.sparse import hstack

from sklearn.metrics.pairwise import cosine_similarity


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

ENCODER_PATH = (
    BASE_DIR
    / "models"
    / "encoder.pkl"
)


# =========================================
# LOAD DATASETS
# =========================================

# =========================================
# LOAD RESOURCES
# =========================================

def load_resources():
    """
    Load project resources once.

    Returns
    -------
    cleaned_df
    encoder
    feature_matrix
    feature_columns
    """

    print("\nLoading project resources...")

    cleaned_df = pd.read_csv(CLEANED_DATA_PATH)

    encoder = joblib.load(ENCODER_PATH)

    print("Encoding restaurant features...")

    categorical_matrix = encoder.transform(
        cleaned_df[
            [
                "city",
                "cuisine"
            ]
        ]
    )

    numerical_matrix = csr_matrix(
        cleaned_df[
            [
                "rating",
                "rating_count",
                "cost"
            ]
        ].values
    )

    feature_matrix = hstack(
        [
            categorical_matrix,
            numerical_matrix
        ]
    ).tocsr()

    print("\nResources loaded successfully.")

    print(f"Restaurants : {len(cleaned_df):,}")

    print(
        f"Features : {feature_matrix.shape[1]:,}"
    )

    return (
        cleaned_df,
        encoder,
        feature_matrix,
        )


(
    cleaned_df,
    encoder,
    feature_matrix,
   ) = load_resources()


# =========================================
# RECOMMENDATION FUNCTION
# =========================================

def recommend_restaurants(
    city,
    cuisine,
    rating,
    rating_count,
    cost,
    top_n=5
):
    # -------------------------------------
    # Clean User Input
    # -------------------------------------

    city = city.strip()

    cuisine = cuisine.strip()
    
    # -------------------------------------
    # Validate Inputs
    # -------------------------------------

    rating = max(0.0, min(float(rating), 5.0))

    rating_count = max(0, int(rating_count))

    cost = max(0.0, float(cost))

    # -------------------------------------
    # Create User Input DataFrame
    # -------------------------------------

    user_input = pd.DataFrame({
        "city": [city],
        "cuisine": [cuisine]
    })

    # Encode categorical features (sparse)
    categorical_input = encoder.transform(user_input)

    # Numerical features
    numerical_input = csr_matrix(
        [[rating, rating_count, cost]]
        )

    # Combined sparse feature vector
    user_vector = hstack(
    [
        categorical_input,
        numerical_input
    ]
)
    
    
    # -------------------------------------
    # Add Numerical Features
    # -------------------------------------



    # -------------------------------------
    # FILTER DATASET
    # -------------------------------------

    filtered_df = cleaned_df

    # Filter by City
    city_matches = filtered_df[
        filtered_df["city"].str.lower() == city.lower()
    ]

    if not city_matches.empty:
        filtered_df = city_matches

    # Filter by Cuisine
    cuisine_matches = filtered_df[
        filtered_df["cuisine"].str.lower().str.contains(
            cuisine.lower(),
            na=False
        )
    ]

    if not cuisine_matches.empty:
        filtered_df = cuisine_matches

    filtered_indices = filtered_df.index.tolist()

    filtered_matrix = feature_matrix[
        filtered_indices
    ]

    # -------------------------------------
    # Calculate Similarity
    # -------------------------------------

    similarity_scores = cosine_similarity(
        user_vector,
        filtered_matrix
    ).flatten()

    # -------------------------------------
    # Get Top Recommendations
    # -------------------------------------

    similarity_df = pd.DataFrame({
    "original_index": filtered_indices,
    "similarity": similarity_scores
    })
    
    # Remove weak matches

    similarity_df = similarity_df[
    similarity_df["similarity"] >= 0.40
    ]

    top_indices = similarity_df.head(top_n)[
        "original_index"
    ].tolist()

    recommendations = cleaned_df.loc[
        top_indices,
        [
            "name",
            "city",
            "cuisine",
            "rating",
            "rating_count",
            "cost"
        ]
    ].copy()

    recommendations["similarity"] = similarity_df.head(top_n)[
        "similarity"
    ].values

    recommendations = recommendations.sort_values(
        by=[
            "similarity",
            "rating"
        ],
        ascending=[
            False,
            False
        ]
    )
    recommendations = recommendations.drop_duplicates(
        subset=["name"]
    )

    if recommendations.empty:

        print("\nNo matching restaurants found.")

        return pd.DataFrame()

    return recommendations.reset_index(drop=True)


# =========================================
# TEST RECOMMENDATION SYSTEM
# =========================================

# =========================================
# TEST RECOMMENDATION SYSTEM
# =========================================

if __name__ == "__main__":

    print("\nTesting Recommendation Engine...")

    results = recommend_restaurants(
        city="Mylapore,Chennai",
        cuisine="South Indian",
        rating=4.2,
        rating_count=100,
        cost=300,
        top_n=5
    )

    print("\nRecommended Restaurants:\n")
    print(results)