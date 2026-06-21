import streamlit as st
import pandas as pd

from sklearn.metrics.pairwise import cosine_similarity


# =========================================
# PAGE CONFIGURATION
# =========================================

st.set_page_config(
    page_title="Swiggy Recommendation System",
    page_icon="🍽️",
    layout="wide"
)


# =========================================
# LOAD DATASETS
# =========================================

@st.cache_data
def load_data():

    cleaned_df = pd.read_csv(
        "data/processed/cleaned_data.csv"
    )

    encoded_df = pd.read_csv(
        "data/processed/encoded_data.csv"
    )

    return cleaned_df, encoded_df


cleaned_df, encoded_df = load_data()


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
        return pd.DataFrame()

    restaurant_index = matches.index[0]


    # -------------------------------------
    # Get Selected Restaurant Vector
    # -------------------------------------

    selected_vector = encoded_df.iloc[
        restaurant_index
    ].values.reshape(1, -1)


    # -------------------------------------
    # Calculate Similarity
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
    # Sort Recommendations
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
# STREAMLIT UI
# =========================================

st.title("🍽️ Swiggy Restaurant Recommendation System")

st.markdown("""
Discover restaurants similar to your favorite restaurant using
Machine Learning and Cosine Similarity.
""")


# =========================================
# RESTAURANT SELECTION
# =========================================

restaurant_list = sorted(
    cleaned_df['name'].unique()
)

selected_restaurant = st.selectbox(
    "Select a Restaurant",
    restaurant_list
)


# =========================================
# RECOMMEND BUTTON
# =========================================

if st.button("Get Recommendations"):

    recommendations = recommend_restaurants(
        selected_restaurant
    )

    st.subheader("Recommended Restaurants")


    # -------------------------------------
    # Display Recommendations
    # -------------------------------------

    for _, row in recommendations.iterrows():

        with st.container():

            st.markdown("---")

            st.markdown(
                f"""
                ### {row['name']}

                📍 **City:** {row['city']}

                🍴 **Cuisine:** {row['cuisine']}

                ⭐ **Rating:** {row['rating']}

                💰 **Cost:** ₹{row['cost']}
                """
            )