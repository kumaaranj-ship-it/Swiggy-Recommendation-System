import streamlit as st
import pandas as pd
import os
import sys
from pathlib import Path

# =====================================================
# PROJECT ROOT
# =====================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

# =====================================================
# IMPORT BACKEND
# =====================================================

from scripts.recommendation_engine import recommend_restaurants

# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Swiggy Restaurant Recommendation System",
    page_icon="🍽️",
    layout="wide"
)

# =====================================================
# REQUIRED FILES
# =====================================================

REQUIRED_FILES = [
    PROJECT_ROOT / "data" / "processed" / "cleaned_data.csv",
    PROJECT_ROOT / "data" / "processed" / "encoded_data.csv",
    PROJECT_ROOT / "models" / "encoder.pkl"
]

missing_files = [
    str(file)
    for file in REQUIRED_FILES
    if not file.exists()
]

if missing_files:

    st.error("❌ Required project files are missing.")

    st.write("Missing Files:")

    for file in missing_files:
        st.write(file)

    st.stop()

# =====================================================
# TITLE
# =====================================================

st.title("🍽️ Swiggy Restaurant Recommendation System")

st.markdown("""
Discover restaurants based on your preferred **City**, **Cuisine**,
**Rating**, and **Budget** using **Machine Learning** and
**Cosine Similarity**.
""")

# =====================================================
# LOAD CLEANED DATA
# =====================================================

@st.cache_data
def load_cleaned_data():

    return pd.read_csv(
        PROJECT_ROOT / "data" / "processed" / "cleaned_data.csv"
    )


cleaned_df = load_cleaned_data()


# =====================================================
# SIDEBAR FILTERS
# =====================================================

st.sidebar.header("🍴 Restaurant Preferences")

# -----------------------------------
# City
# -----------------------------------

city_list = sorted(
    cleaned_df["city"].dropna().unique().tolist()
)

selected_city = st.sidebar.selectbox(
    "Select City",
    city_list
)

# -----------------------------------
# Cuisine
# -----------------------------------

city_df = cleaned_df[
    cleaned_df["city"] == selected_city
]

cuisine_set = set()

for cuisines in city_df["cuisine"].dropna():

    for cuisine in cuisines.split(","):

        cuisine_set.add(
            cuisine.strip()
        )

cuisine_list = sorted(cuisine_set)

selected_cuisine = st.sidebar.selectbox(
    "Select Cuisine",
    cuisine_list
)

# -----------------------------------
# Rating
# -----------------------------------

selected_rating = st.sidebar.slider(
    "Minimum Rating",
    min_value=0.0,
    max_value=5.0,
    value=4.0,
    step=0.1
)

# -----------------------------------
# Rating Count
# -----------------------------------

selected_rating_count = st.sidebar.number_input(
    "Minimum Rating Count",
    min_value=0,
    value=50,
    step=10
)

# -----------------------------------
# Budget
# -----------------------------------

selected_cost = st.sidebar.slider(
    "Maximum Budget (₹)",
    min_value=50,
    max_value=2000,
    value=300,
    step=50
)

city = selected_city
cuisine = selected_cuisine
rating = selected_rating
rating_count = selected_rating_count
budget = selected_cost



col_left, col_center, col_right = st.columns([1, 2, 1])

with col_center:
    get_recommendations = st.sidebar.button(
        "🍽️ Get Recommendations",
        use_container_width=True,
        type="primary"
    )
    
if get_recommendations:

    with st.spinner("Finding the best restaurants for you..."):

        recommendations = recommend_restaurants(
            city=city,
            cuisine=cuisine,
            rating=rating,
            rating_count=rating_count,
            cost=budget,
            top_n=10
        )
        
        if recommendations.empty:

            st.warning("""
### No restaurants matched your current preferences.

Try one of these:

• Increase your budget

• Lower the minimum rating

• Select another cuisine

• Try another city
"""
    )
        else:
            st.success(
                f"Found {len(recommendations)} restaurant(s) matching your preferences."
            )
            csv = recommendations.to_csv(index=False).encode("utf-8")

            st.download_button(
                label="📥 Download Recommendations (CSV)",
                data=csv,
                file_name="restaurant_recommendations.csv",
                mime="text/csv",
                )
            
            st.subheader("📊 Recommendation Dashboard")

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric(
                    "🍴 Restaurants",
                    len(recommendations)
                )

            with col2:
                st.metric(
                    "⭐ Avg Rating",
                    f"{recommendations['rating'].mean():.2f}"
                )

            with col3:
                st.metric(
                    "💰 Avg Budget",
                    f"₹{recommendations['cost'].mean():,.0f}"
                )

            with col4:
                st.metric(
                    "📍 City",
                    city
                )

            st.divider()
            
            for rank, (_, row) in enumerate(recommendations.iterrows(), start=1):

                card = st.container(border=True)

                with card:

                    medals = {
                        1: "🥇",
                        2: "🥈",
                        3: "🥉"
                    }

                    badge = medals.get(rank, "🍽️")

                    st.markdown(
                        f"## {badge} #{rank} {row['name']}"
                    )

                    col1, col2 = st.columns(2)

                    with col1:
                        st.write(f"**City:** {row['city']}")
                        cuisine = row["cuisine"]
                        if len(cuisine) > 55:
                            cuisine = cuisine[:55] + "..."
                        st.write(f"**Cuisine:** {cuisine}")    
                        st.write(f"**Budget:** ₹{row['cost']:,.0f}")

                    with col2:
                        if row["rating"] >= 4.5:
                            rating_icon = "🟢"

                        elif row["rating"] >= 4.0:
                            rating_icon = "🟡"

                        else:
                            rating_icon = "🔴"
                        st.write(
                                f"**Rating:** {rating_icon} ⭐ {row['rating']:.1f}"
                                )
                        st.write(f"**Rating Count:** {int(row['rating_count']):,}")
                        st.write(
                            f"**Similarity Score:** {row['similarity'] * 100:.1f}%"
                            )
                        st.progress(float(row["similarity"]))

                    st.divider()
                    st.caption(
                    "Swiggy Restaurant Recommendation System | "
                    "Built with Streamlit, Scikit-learn, OneHotEncoder & Cosine Similarity"
                    )
                    st.success(
                    "Recommendation engine executed successfully."
                    )
                    
