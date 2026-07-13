# ==========================================
# Hybrid Recommendation Engine
# ==========================================
#
# This module generates personalized
# restaurant recommendations by combining:
#
# • User Preferences
# • Content-Based Recommendation
# • Collaborative Filtering
# • Restaurant Ratings
#
# ==========================================

import sqlite3

from collections import Counter
from collections import defaultdict


# ==========================================
# Database Location
# ==========================================

DATABASE = "database/swiggy.db"


# ==========================================
# Recommendation Weights
# ==========================================

PREFERENCE_WEIGHT = 0.50
COLLABORATIVE_WEIGHT = 0.30
RATING_WEIGHT = 0.20


# ==========================================
# Database Connection
# ==========================================

def get_connection():
    """
    Create and return a SQLite connection.
    """

    return sqlite3.connect(DATABASE)

# ==========================================
# Load Restaurants
# ==========================================

def load_restaurants():
    """
    Load all restaurants from the database.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            restaurant_id,
            name,
            city,
            cuisine,
            rating,
            rating_count,
            cost,
            address
        FROM restaurants
    """)

    rows = cursor.fetchall()

    conn.close()

    restaurants = []

    for row in rows:

        restaurant = {

            "restaurant_id": row[0],

            "restaurant_name": row[1],

            "city": row[2],

            "cuisine": row[3],

            "rating": row[4],

            "rating_count": row[5],

            "cost": row[6],

            "address": row[7]

        }

        restaurants.append(restaurant)

    return restaurants


# ==========================================
# Load User Preferences
# ==========================================

def load_user_preferences(user_id):
    """
    Load the saved preference scores
    for the given user.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            preference_type,
            preference_value,
            score
        FROM user_preferences
        WHERE user_id = ?
    """, (user_id,))

    rows = cursor.fetchall()

    conn.close()

    preferences = {
        "city": {},
        "cuisine": {},
        "budget": {},
        "rating": {}
    }

    for preference_type, preference_value, score in rows:

        if preference_type not in preferences:
            preferences[preference_type] = {}

        preferences[preference_type][preference_value] = score

    return preferences
# ==========================================
# Calculate Preference Score
# ==========================================

def calculate_preference_score(
    restaurant,
    preferences
):
    """
    Calculate the preference score for
    a single restaurant.
    """

    score = 0

    # -------------------------
    # City Score
    # -------------------------

    city = restaurant["city"]

    if city in preferences["city"]:
        score += preferences["city"][city]

    # -------------------------
    # Cuisine Score
    # -------------------------

    cuisine = restaurant["cuisine"]

    if cuisine in preferences["cuisine"]:
        score += preferences["cuisine"][cuisine]

    # -------------------------
    # Budget Score
    # -------------------------

    budget = str(restaurant["cost"])

    if budget in preferences["budget"]:
        score += preferences["budget"][budget]

    # -------------------------
    # Rating Score
    # -------------------------

    rating = str(restaurant["rating"])

    if rating in preferences["rating"]:
        score += preferences["rating"][rating]

    return score


# ==========================================
# Calculate Content Scores
# ==========================================

def calculate_content_scores(
    restaurants,
    preferences
):
    """
    Calculate preference scores for
    all restaurants.
    """

    scored_restaurants = []

    for restaurant in restaurants:

        preference_score = calculate_preference_score(
            restaurant,
            preferences
        )

        restaurant_copy = restaurant.copy()

        restaurant_copy["preference_score"] = preference_score

        scored_restaurants.append(restaurant_copy)

    return scored_restaurants

# ==========================================
# Load Preferences of All Users
# ==========================================

def load_all_user_preferences():
    """
    Load preferences for every user.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            user_id,
            preference_type,
            preference_value,
            score
        FROM user_preferences
    """)

    rows = cursor.fetchall()

    conn.close()

    all_preferences = defaultdict(
        lambda: {
            "city": {},
            "cuisine": {},
            "budget": {},
            "rating": {}
        }
    )

    for user_id, preference_type, preference_value, score in rows:

        all_preferences[user_id][preference_type][preference_value] = score

    return dict(all_preferences)


# ==========================================
# Calculate User Similarity
# ==========================================

def calculate_user_similarity(
    current_preferences,
    other_preferences
):
    """
    Calculate similarity between two users.
    """

    similarity = 0

    preference_types = [
        "city",
        "cuisine",
        "budget",
        "rating"
    ]

    for preference_type in preference_types:

        current_values = current_preferences.get(
            preference_type,
            {}
        )

        other_values = other_preferences.get(
            preference_type,
            {}
        )

        for value in current_values:

            if value in other_values:
                similarity += min(
                    current_values[value],
                    other_values[value]
                )

    return similarity


# ==========================================
# Calculate Collaborative Scores
# ==========================================

def calculate_collaborative_scores(
    user_id,
    restaurants,
    current_preferences
):
    """
    Calculate collaborative scores for
    every restaurant.
    """

    all_preferences = load_all_user_preferences()

    if len(all_preferences) <= 1:

        print(
            "Users available for collaborative filtering:",
            len(all_preferences)
        )

        print(
            "Only one user exists in the system."
        )

        print(
            "Collaborative filtering requires at least two users."
        )

        updated_restaurants = []

        for restaurant in restaurants:

            restaurant_copy = restaurant.copy()

            restaurant_copy["collaborative_score"] = 0

            updated_restaurants.append(
                restaurant_copy
            )

        return updated_restaurants

    print(
        "Users available for collaborative filtering:",
        len(all_preferences)
    )

    collaborative_scores = {}
    similarity_totals = {}

    for restaurant in restaurants:
        collaborative_scores[restaurant["restaurant_id"]] = 0
        similarity_totals[restaurant["restaurant_id"]] = 0.0

    for other_user_id, other_preferences in all_preferences.items():

        if other_user_id == user_id:
            continue

        similarity = calculate_user_similarity(
            current_preferences,
            other_preferences
        )

        if similarity == 0:
            continue

        for restaurant in restaurants:

            score = 0

            if restaurant["city"] in other_preferences["city"]:
                score += other_preferences["city"][restaurant["city"]]

            if restaurant["cuisine"] in other_preferences["cuisine"]:
                score += other_preferences["cuisine"][restaurant["cuisine"]]

            budget = str(restaurant["cost"])

            if budget in other_preferences["budget"]:
                score += other_preferences["budget"][budget]

            rating = str(restaurant["rating"])

            if rating in other_preferences["rating"]:
                score += other_preferences["rating"][rating]
                
            restaurant_id = restaurant["restaurant_id"]
            collaborative_scores[restaurant["restaurant_id"]] += (
                similarity * score
            )
            similarity_totals[restaurant_id] += similarity

    updated_restaurants = []

    for restaurant in restaurants:

        restaurant_copy = restaurant.copy()

        restaurant_id = restaurant["restaurant_id"]

        if similarity_totals[restaurant_id] > 0:

            collaborative_score = (
            collaborative_scores[restaurant_id]
            / similarity_totals[restaurant_id]
        )

        else:

            collaborative_score = 0

        restaurant_copy["collaborative_score"] = round(
            collaborative_score,
            3
        )

        updated_restaurants.append(
            restaurant_copy
        )

    return updated_restaurants

# ==========================================================
# CALCULATE HYBRID SCORES
# ==========================================================

def calculate_hybrid_scores(restaurants):
    """
    Combines:
    1. Preference Score
    2. Collaborative Score
    3. Restaurant Rating

    Returns the restaurant list with
    hybrid_score added.
    """

    for restaurant in restaurants:

        # ------------------------------------------
        # Preference Score
        # ------------------------------------------

        preference_score = restaurant.get(
            "preference_score",
            0
        )

        # ------------------------------------------
        # Collaborative Score
        # ------------------------------------------

        collaborative_score = restaurant.get(
            "collaborative_score",
            0
        )

        # ------------------------------------------
        # Restaurant Rating Score
        # ------------------------------------------

        rating_score = restaurant.get(
            "rating",
            0
        )

        # ------------------------------------------
        # Calculate Hybrid Score
        # ------------------------------------------

        hybrid_score = (

            (preference_score * PREFERENCE_WEIGHT)

            +

            (collaborative_score * COLLABORATIVE_WEIGHT)

            +

            (rating_score * RATING_WEIGHT)

        )

        # ------------------------------------------
        # Save Hybrid Score
        # ------------------------------------------

        restaurant["hybrid_score"] = round(
            hybrid_score,
            3
        )

    return restaurants


# ==========================================================
# SORT RESTAURANTS BY HYBRID SCORE
# ==========================================================

def rank_restaurants(restaurants):
    """
    Sorts restaurants based on
    hybrid score in descending order.
    """

    ranked_restaurants = sorted(

        restaurants,

        key=lambda restaurant: restaurant["hybrid_score"],

        reverse=True

    )

    return ranked_restaurants

# ==========================================================
# HYBRID RECOMMENDATION PIPELINE
# ==========================================================

def recommend_restaurants(user_id, top_n=10):
    """
    Generates restaurant recommendations
    for the given user.

    Workflow:
    1. Load restaurants
    2. Load user preferences
    3. Calculate preference scores
    4. Calculate collaborative scores
    5. Calculate hybrid scores
    6. Rank restaurants
    7. Return ranked list
    """

    # ------------------------------------------
    # Load Restaurant Data
    # ------------------------------------------

    restaurants = load_restaurants()

    if len(restaurants) == 0:

        return []

    # ------------------------------------------
    # Load User Preferences
    # ------------------------------------------

    user_preferences = load_user_preferences(
        user_id
    )

    # ------------------------------------------
    # Calculate Preference Scores
    # ------------------------------------------

    restaurants = calculate_content_scores(
        restaurants,
        user_preferences
    )

    # ------------------------------------------
    # Calculate Collaborative Scores
    # ------------------------------------------

    restaurants = calculate_collaborative_scores(
        user_id,
        restaurants,
        user_preferences
    )

    # ------------------------------------------
    # Calculate Hybrid Scores
    # ------------------------------------------

    restaurants = calculate_hybrid_scores(
        restaurants
    )

    # ------------------------------------------
    # Rank Restaurants
    # ------------------------------------------

    ranked_restaurants = rank_restaurants(
        restaurants
    )

    # ------------------------------------------
    # Return Ranked Restaurants
    # ------------------------------------------

    return ranked_restaurants[:top_n]

# ==========================================================
# MAIN FUNCTION
# ==========================================================

def main():

    print("=" * 60)
    print("Hybrid Restaurant Recommendation System")
    print("=" * 60)

    # ------------------------------------------
    # Get User ID
    # ------------------------------------------

    user_input = input("\nEnter User ID : ")

    if not user_input.isdigit():
    
        print("\nInvalid User ID.")
        print("Please enter a numeric User ID.")

        return

    user_id = int(user_input)

    # ------------------------------------------
    # Generate Recommendations
    # ------------------------------------------

    recommendations = recommend_restaurants(
        user_id
    )

    # ------------------------------------------
    # Check Results
    # ------------------------------------------

    if len(recommendations) == 0:

        print("\nNo restaurants available.")

        return

    # ------------------------------------------
    # Display Recommendations
    # ------------------------------------------

    print("\nTop Restaurant Recommendations")
    print("-" * 60)

    top_recommendations = recommendations[:10]

    for index, restaurant in enumerate(
        top_recommendations,
        start=1
    ):

        print(f"\n{index}. {restaurant['restaurant_name']}")

        print(f"City                 : {restaurant['city']}")

        print(f"Cuisine              : {restaurant['cuisine']}")

        print(f"Cost                 : ₹{restaurant['cost']}")

        print(f"Rating               : {restaurant['rating']}")

        print(
            f"Preference Score     : "
            f"{restaurant['preference_score']}"
        )

        print(
            f"Collaborative Score  : "
            f"{restaurant['collaborative_score']}"
        )

        print(
            f"Hybrid Score         : "
            f"{restaurant['hybrid_score']}"
        )

        print("-" * 60)


# ==========================================================
# PROGRAM ENTRY
# ==========================================================

if __name__ == "__main__":
    main()