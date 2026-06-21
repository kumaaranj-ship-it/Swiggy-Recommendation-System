import pandas as pd

from sklearn.metrics.pairwise import cosine_similarity


# =========================================
# FILE PATHS
# =========================================

CLEANED_DATA_PATH = "data/processed/cleaned_data.csv"

ENCODED_DATA_PATH = "data/processed/encoded_data.csv"


# =========================================
# LOAD DATASETS
# =========================================

print("\nLoading datasets...")

cleaned_df = pd.read_csv(CLEANED_DATA_PATH)

encoded_df = pd.read_csv(ENCODED_DATA_PATH)

print("Datasets loaded successfully.")

print("\nCleaned Dataset Shape:")
print(cleaned_df.shape)

print("\nEncoded Dataset Shape:")
print(encoded_df.shape)


# =========================================
# RECOMMENDATION FUNCTION
# =========================================

def recommend_restaurants(
    restaurant_name,
    top_n=5
):

    # -------------------------------------
    # Find Restaurant Index
    # -------------------------------------

    matches = cleaned_df[
        cleaned_df['name']
        .str.lower()
        == restaurant_name.lower()
    ]

    if matches.empty:

        print(f"\nRestaurant '{restaurant_name}' not found.")

        return None

    restaurant_index = matches.index[0]

    print(f"\nRestaurant Index: {restaurant_index}")


    # -------------------------------------
    # Get Selected Restaurant Vector
    # -------------------------------------

    selected_vector = encoded_df.iloc[
        restaurant_index
    ].values.reshape(1, -1)


    # -------------------------------------
    # Calculate Similarity Dynamically
    # -------------------------------------

    similarity_scores = cosine_similarity(
        selected_vector,
        encoded_df
    )[0]


    # -------------------------------------
    # Create Similarity DataFrame
    # -------------------------------------

    similarity_df = pd.DataFrame({
        'index': cleaned_df.index,
        'similarity': similarity_scores
    })


    # -------------------------------------
    # Remove Same Restaurant
    # -------------------------------------

    similarity_df = similarity_df[
        similarity_df['index'] != restaurant_index
    ]


    # -------------------------------------
    # Get Top Recommendations
    # -------------------------------------

    similarity_df = similarity_df.sort_values(
        by='similarity',
        ascending=False
    )

    top_indices = similarity_df.head(top_n)['index']


    # -------------------------------------
    # Fetch Restaurant Details
    # -------------------------------------

    recommendations = cleaned_df.loc[
        top_indices,
        [
            'name',
            'city',
            'cuisine',
            'rating',
            'cost'
        ]
    ]

    return recommendations


# =========================================
# TEST RECOMMENDATION SYSTEM
# =========================================

sample_restaurant = cleaned_df['name'].iloc[0]

print(f"\nTesting recommendation system using:")
print(sample_restaurant)

results = recommend_restaurants(sample_restaurant)

print("\nRecommended Restaurants:")
print(results)