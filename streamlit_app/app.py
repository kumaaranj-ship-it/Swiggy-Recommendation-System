import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# =====================================================
# PROJECT ROOT
# =====================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

# =====================================================
# IMPORT BACKEND MODULES
# =====================================================

from scripts.recommendation_engine import recommend_restaurants
from scripts.hybrid_recommender import (
    recommend_restaurants as hybrid_recommendations
)
from scripts.user_auth import (
    register_user,
    login_user,
    current_user
)

from scripts.interaction_logger import (
    log_search,
    log_click,
    add_favourite,
    remove_favourite,
    already_favourite,
    rate_restaurant
)

from scripts.user_auth import (
    login_user,
    register_user,
    logout_user,
    get_current_user
)

# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Swiggy Restaurant Recommendation System",
    page_icon="🍽️",
    layout="wide"
)

# ==========================================================
# Session State Initialization
# ==========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "username" not in st.session_state:
    st.session_state.username = "Guest"

if "current_user" not in st.session_state:

    st.session_state.current_user = None

# =====================================================
# VERIFY REQUIRED PROJECT FILES
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

    st.error("Required project files are missing.")

    st.write("Missing Files:")

    for file in missing_files:
        st.write(file)

    st.stop()

# =====================================================
# APPLICATION TITLE
# =====================================================

st.title("🍽️ Swiggy Restaurant Recommendation System")

st.markdown(
"""
Discover restaurants based on your preferred
**City**, **Cuisine**, **Rating** and **Budget**
using Machine Learning and Cosine Similarity.
"""
)

# =====================================================
# LOAD DATA
# =====================================================

@st.cache_data
def load_cleaned_data():

    dataframe = pd.read_csv(
        PROJECT_ROOT /
        "data" /
        "processed" /
        "cleaned_data.csv"
    )

    return dataframe


cleaned_df = load_cleaned_data()

print("\n===== CLEANED DATA COLUMNS =====")
print(cleaned_df.columns.tolist())
print("===============================\n")

# =====================================================
# CURRENT USER
# =====================================================

current_user = get_current_user()

if current_user:

    user_id = current_user["user_id"]

    username = current_user["username"]

else:

    user_id = None

    username = "Guest"

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.header("Restaurant Preferences")

recommendation_mode = st.sidebar.radio(
    "Recommendation Mode",
    [
        "Content Based",
        "Hybrid Personalized"
    ]
)

st.sidebar.write(f"Logged in as: **{username}**")

# ==========================================================
# Login Section
# ==========================================================

if not st.session_state.logged_in:

    st.sidebar.markdown("---")
    st.sidebar.subheader("🔐 Login")

    login_username = st.sidebar.text_input(
        "Username",
        key="login_username"
    )

    login_password = st.sidebar.text_input(
        "Password",
        type="password",
        key="login_password"
    )

    if st.sidebar.button("Login"):

        success, message = login_user(
        login_username,
        login_password
    )

        if success:

            st.session_state.logged_in = True

            st.session_state.username = login_username

            st.sidebar.success(message)

            st.rerun()

        else:
        
            st.sidebar.error(message)

# -----------------------------------------------------
# CITY
# -----------------------------------------------------

city_list = sorted(
    cleaned_df["city"]
    .dropna()
    .unique()
    .tolist()
)

selected_city = st.sidebar.selectbox(
    "Select City",
    city_list
)

# -----------------------------------------------------
# CUISINE
# -----------------------------------------------------

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

# -----------------------------------------------------
# MINIMUM RATING
# -----------------------------------------------------

selected_rating = st.sidebar.slider(
    "Minimum Rating",
    min_value=0.0,
    max_value=5.0,
    value=4.0,
    step=0.1
)

# -----------------------------------------------------
# MINIMUM RATING COUNT
# -----------------------------------------------------

selected_rating_count = st.sidebar.number_input(
    "Minimum Rating Count",
    min_value=0,
    value=50,
    step=10
)

# -----------------------------------------------------
# MAXIMUM BUDGET
# -----------------------------------------------------

selected_budget = st.sidebar.slider(
    "Maximum Budget (₹)",
    min_value=50,
    max_value=2000,
    value=300,
    step=50
)

# =====================================================
# USER INPUTS
# =====================================================

city = selected_city

cuisine = selected_cuisine

rating = selected_rating

rating_count = selected_rating_count

budget = selected_budget

# =====================================================
# GET RECOMMENDATIONS BUTTON
# =====================================================

get_recommendations = st.sidebar.button(

    "🍽️ Get Recommendations",

    use_container_width=True,

    type="primary"
)
# =====================================================
# GENERATE RECOMMENDATIONS
# =====================================================

if get_recommendations:

    with st.spinner("Finding the best restaurants for you..."):

        # ---------------------------------------------
        # Generate Recommendations
        # ---------------------------------------------

        if recommendation_mode == "Content Based":
        

            recommendations = recommend_restaurants(
                city=city,
                cuisine=cuisine,
                rating=rating,
                rating_count=rating_count,
                cost=budget,
                top_n=10
            )

        else:
            if user_id is None:

                st.warning(
                "Please login to use Hybrid Personalized Recommendations."
            )
                st.stop()

            recommendations = hybrid_recommendations(
            user_id
            )

        # Keep only the Top 10 recommendations
        recommendations = recommendations[:10]

        recommendations = pd.DataFrame(recommendations)

        # Make Hybrid output compatible with the existing UI
        if "restaurant_name" in recommendations.columns:
            recommendations.rename(
            columns={"restaurant_name": "name"},
            inplace=True
            )

        if (
            "hybrid_score" in recommendations.columns
            and not recommendations.empty
            ):
            max_score = recommendations["hybrid_score"].max()

        if max_score > 0:
            recommendations["similarity"] = (
            recommendations["hybrid_score"] / max_score
        )
        else:
            recommendations["similarity"] = 0
            

            # Convert hybrid recommendations to DataFrame
            recommendations = pd.DataFrame(recommendations)
            # Make hybrid output compatible with the existing UI
            if "restaurant_name" in recommendations.columns:
                recommendations.rename(
                columns={
                "restaurant_name": "name"
                },
            inplace=True
            )

            if "hybrid_score" in recommendations.columns:
                recommendations["similarity"] = (
                recommendations["hybrid_score"]
                / recommendations["hybrid_score"].max()
            )
    

        # ---------------------------------------------
        # Log Search History
        # ---------------------------------------------

        if user_id is not None:

            search_keyword = (
            f"{city} | "
            f"{cuisine} | "
            f"Rating >= {rating} | "
            f"Reviews >= {rating_count} | "
            f"Budget <= ₹{budget}"
        )
            log_search(
                user_id=user_id,
                keyword=search_keyword
            )

        # ---------------------------------------------
        # No Recommendations Found
        # ---------------------------------------------

        if recommendations.empty:

            st.warning(
                """
### No restaurants matched your preferences.

Try one of these:

• Increase your budget

• Lower the minimum rating

• Reduce the minimum rating count

• Try another cuisine

• Select another city
"""
            )

        # ---------------------------------------------
        # Recommendations Available
        # ---------------------------------------------

        else:

            st.success(
                f"Found {len(recommendations)} restaurant(s) matching your preferences."
            )

            # -----------------------------------------
            # Download CSV
            # -----------------------------------------

            csv = recommendations.to_csv(
                index=False
            ).encode("utf-8")

            st.download_button(
                label="📥 Download Recommendations",
                data=csv,
                file_name="restaurant_recommendations.csv",
                mime="text/csv"
            )

            # -----------------------------------------
            # Dashboard Metrics
            # -----------------------------------------

            st.subheader("📊 Recommendation Dashboard")

            metric1, metric2, metric3, metric4 = st.columns(4)

            with metric1:

                st.metric(
                    "Restaurants",
                    len(recommendations)
                )

            with metric2:

                st.metric(
                    "Average Rating",
                    f"{recommendations['rating'].mean():.2f}"
                )

            with metric3:

                st.metric(
                    "Average Budget",
                    f"₹{recommendations['cost'].mean():,.0f}"
                )

            with metric4:

                st.metric(
                    "Selected City",
                    city
                )

            st.divider()

            # -----------------------------------------
            # Restaurant Cards
            # -----------------------------------------

            for rank, (_, row) in enumerate(
                recommendations.iterrows(),
                start=1
            ):
                                # =====================================================
                # RESTAURANT CARD
                # =====================================================

                card = st.container(border=True)

                with card:

                    # ---------------------------------------------
                    # Ranking Badge
                    # ---------------------------------------------

                    medals = {
                        1: "🥇",
                        2: "🥈",
                        3: "🥉"
                    }

                    badge = medals.get(rank, "🍽️")

                    st.markdown(
                        f"## {badge} #{rank} {row['name']}"
                    )

                    # ---------------------------------------------
                    # Restaurant Information
                    # ---------------------------------------------

                    info_col1, info_col2 = st.columns(2)

                    with info_col1:

                        st.write(f"**City:** {row['city']}")

                        cuisine_text = row["cuisine"]

                        if len(cuisine_text) > 60:
                            cuisine_text = cuisine_text[:60] + "..."

                        st.write(f"**Cuisine:** {cuisine_text}")

                        st.write(f"**Budget:** ₹{row['cost']:,.0f}")

                    with info_col2:

                        if row["rating"] >= 4.5:
                            rating_icon = "🟢"

                        elif row["rating"] >= 4.0:
                            rating_icon = "🟡"

                        else:
                            rating_icon = "🔴"

                        st.write(
                            f"**Rating:** {rating_icon} ⭐ {row['rating']:.1f}"
                        )

                        st.write(
                            f"**Rating Count:** {int(row['rating_count']):,}"
                        )

                        st.write(
                            f"**Similarity Score:** {row['similarity'] * 100:.1f}%"
                        )

                        st.progress(float(row["similarity"]))

                    st.divider()

                    # =====================================================
                    # USER ACTIONS
                    # =====================================================

                    action_col1, action_col2, action_col3 = st.columns(3)

                    # -----------------------------------------------------
                    # VIEW RESTAURANT
                    # -----------------------------------------------------

                    with action_col1:

                        if st.button(
                            "👀 View",
                            key=f"view_{row['restaurant_id']}"
                        ):

                            if user_id is not None:

                                log_click(
                                    user_id=user_id,
                                    restaurant_id=row["restaurant_id"]
                                )

                                st.success(
                                    "Restaurant interaction recorded."
                                )

                    # -----------------------------------------------------
                    # FAVOURITE
                    # -----------------------------------------------------

                    with action_col2:

                        if user_id is not None:

                            favourite = already_favourite(
                                user_id=user_id,
                                restaurant_id=row["restaurant_id"]
                            )

                            if favourite:

                                if st.button(
                                    "💔 Remove Favourite",
                                    key=f"remove_{row['restaurant_id']}"
                                ):

                                    remove_favourite(
                                        user_id=user_id,
                                        restaurant_id=row["restaurant_id"]
                                    )

                                    st.success(
                                        "Removed from favourites."
                                    )

                            else:

                                if st.button(
                                    "❤️ Add Favourite",
                                    key=f"add_{row['restaurant_id']}"
                                ):

                                    add_favourite(
                                        user_id=user_id,
                                        restaurant_id=row["restaurant_id"]
                                    )

                                    st.success(
                                        "Added to favourites."
                                    )

                    # -----------------------------------------------------
                    # RATE RESTAURANT
                    # -----------------------------------------------------

                    with action_col3:

                        if user_id is not None:

                            user_rating = st.selectbox(
                                "Rate",
                                [1, 2, 3, 4, 5],
                                index=4,
                                key=f"rating_{row['restaurant_id']}"
                            )

                            if st.button(
                                "⭐ Submit",
                                key=f"submit_{row['restaurant_id']}"
                            ):

                                rate_restaurant(
                                    user_id=user_id,
                                    restaurant_id=row["restaurant_id"],
                                    rating=user_rating
                                )

                                st.success(
                                    "Rating submitted."
                                )

                    st.divider()

                    st.caption(
                        "Swiggy Restaurant Recommendation System | "
                        "Built with Streamlit, Scikit-learn, "
                        "OneHotEncoder & Cosine Similarity"
                    )

                    st.success(
                        "Recommendation generated successfully."
                    )