# ==========================================
# Preference Analyzer
# ==========================================
# This module analyzes user behaviour and
# generates preference scores for:
#
# • Cities
# • Cuisines
# • Budget
# • Ratings
#
# The calculated scores are stored in
# user_preferences table.
# ==========================================

import sqlite3
from scripts.database import get_connection
from collections import Counter

# ==========================================
# Database Location
# ==========================================

DATABASE = "database/swiggy.db"


# ==========================================
# Database Connection
# ==========================================

def get_connection():
    """
    Create and return SQLite connection.
    """

    return sqlite3.connect(DATABASE)

# ==========================================
# Clear Existing Preferences
# ==========================================

def clear_preferences(user_id):
    """
    Remove all existing preferences
    for the given user.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM user_preferences
        WHERE user_id = ?
    """, (user_id,))

    conn.commit()
    conn.close()


# ==========================================
# Save One Preference
# ==========================================

def save_preference(
    user_id,
    preference_type,
    preference_value,
    score
):
    """
    Save one preference into the
    user_preferences table.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO user_preferences
        (
            user_id,
            preference_type,
            preference_value,
            score
        )
        VALUES (?, ?, ?, ?)
    """,
    (
        user_id,
        preference_type,
        preference_value,
        score
    ))

    conn.commit()
    conn.close()
    
    # ==========================================
# Analyze Search History
# ==========================================

def analyze_search_history(user_id):
    """
    Analyze the user's search history.

    Every search contributes +1 score.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            r.city,
            r.cuisine,
            r.rating,
            r.cost
        FROM search_history sh
        JOIN restaurants r
            ON
                r.name LIKE '%' || sh.search_query || '%'
                OR r.city LIKE '%' || sh.search_query || '%'
                OR r.cuisine LIKE '%' || sh.search_query || '%'
        WHERE sh.user_id = ?
    """, (user_id,))

    rows = cursor.fetchall()

    conn.close()

    preferences = {
        "city": Counter(),
        "cuisine": Counter(),
        "budget": Counter(),
        "rating": Counter()
    }

    for city, cuisine, rating, cost in rows:

        if city:
            preferences["city"][city] += 1

        if cuisine:
            preferences["cuisine"][cuisine] += 1

        if cost is not None:
            preferences["budget"][str(cost)] += 1

        if rating is not None:
            preferences["rating"][str(rating)] += 1

    return preferences
# ==========================================
# Analyze Click History
# ==========================================

def analyze_click_history(user_id):
    """
    Analyze the user's click history.

    Every click contributes +2 score.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            r.city,
            r.cuisine,
            r.cost,
            r.rating
        FROM click_history ch
        JOIN restaurants r
            ON ch.restaurant_id = r.restaurant_id
        WHERE ch.user_id = ?
    """, (user_id,))

    rows = cursor.fetchall()

    conn.close()

    preferences = {
        "city": Counter(),
        "cuisine": Counter(),
        "budget": Counter(),
        "rating": Counter()
    }

    for city, cuisine, cost, rating in rows:

        if city:
            preferences["city"][city] += 2

        if cuisine:
            preferences["cuisine"][cuisine] += 2

        if cost is not None:
            preferences["budget"][str(cost)] += 2

        if rating is not None:
            preferences["rating"][str(rating)] += 2

    return preferences


# ==========================================
# Analyze Favourites
# ==========================================

def analyze_favourites(user_id):
    """
    Analyze the user's favourite restaurants.

    Every favourite contributes +15 score.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            r.city,
            r.cuisine,
            r.cost,
            r.rating
        FROM favourites f
        JOIN restaurants r
            ON f.restaurant_id = r.restaurant_id
        WHERE f.user_id = ?
    """, (user_id,))

    rows = cursor.fetchall()

    conn.close()

    preferences = {
        "city": Counter(),
        "cuisine": Counter(),
        "budget": Counter(),
        "rating": Counter()
    }

    for city, cuisine, cost, rating in rows:

        if city:
            preferences["city"][city] += 15

        if cuisine:
            preferences["cuisine"][cuisine] += 15

        if cost is not None:
            preferences["budget"][str(cost)] += 15

        if rating is not None:
            preferences["rating"][str(rating)] += 15

    return preferences
# ==========================================
# Analyze Ratings
# ==========================================

def analyze_ratings(user_id):
    """
    Analyze the user's restaurant ratings.

    Every rating contributes:
    rating × 5
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            r.city,
            r.cuisine,
            r.cost,
            r.rating,
            rt.rating
        FROM ratings rt
        JOIN restaurants r
            ON rt.restaurant_id = r.restaurant_id
        WHERE rt.user_id = ?
    """, (user_id,))

    rows = cursor.fetchall()

    conn.close()

    preferences = {
        "city": Counter(),
        "cuisine": Counter(),
        "budget": Counter(),
        "rating": Counter()
    }

    for city, cuisine, cost, restaurant_rating, user_rating in rows:

        score = user_rating * 5

        if city:
            preferences["city"][city] += score

        if cuisine:
            preferences["cuisine"][cuisine] += score

        if cost is not None:
            preferences["budget"][str(cost)] += score

        if restaurant_rating is not None:
            preferences["rating"][str(restaurant_rating)] += score

    return preferences


# ==========================================
# Combine Preference Scores
# ==========================================

def calculate_weighted_scores(*preference_sets):
    """
    Combine multiple preference dictionaries
    into one final weighted score dictionary.
    """

    final_preferences = {
        "city": Counter(),
        "cuisine": Counter(),
        "budget": Counter(),
        "rating": Counter()
    }

    for preference_set in preference_sets:

        for preference_type in final_preferences:

            final_preferences[preference_type].update(
                preference_set[preference_type]
            )

    return final_preferences
# ==========================================
# Generate User Preferences
# ==========================================

def generate_preferences(user_id):
    """
    Generate preference scores for a user
    and save them into user_preferences.
    """

    # Analyze all interactions
    search_preferences = analyze_search_history(user_id)

    click_preferences = analyze_click_history(user_id)

    favourite_preferences = analyze_favourites(user_id)

    rating_preferences = analyze_ratings(user_id)

    # Combine all scores
    final_preferences = calculate_weighted_scores(
        search_preferences,
        click_preferences,
        favourite_preferences,
        rating_preferences
    )

    # Remove old preferences
    clear_preferences(user_id)

    # Save new preferences
    for preference_type, values in final_preferences.items():

        for preference_value, score in values.items():

            save_preference(
                user_id=user_id,
                preference_type=preference_type,
                preference_value=preference_value,
                score=score
            )

    return final_preferences


# ==========================================
# Get Saved Preferences
# ==========================================

def get_preferences(user_id):
    """
    Return all saved preferences
    for a user.
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
        ORDER BY
            preference_type,
            score DESC
    """, (user_id,))

    rows = cursor.fetchall()

    conn.close()

    return rows

# ==========================================
# Load All User IDs
# ==========================================

def load_all_user_ids():
    """
    Load every user ID from
    the users table.
    """

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT user_id
        FROM users
        ORDER BY user_id
        """
    )

    rows = cursor.fetchall()

    conn.close()

    user_ids = []

    for row in rows:

        user_ids.append(row[0])

    return user_ids


# ==========================================
# Main
# ==========================================

def main():

    print("=" * 60)
    print("Generating Preferences")
    print("=" * 60)

    user_ids = load_all_user_ids()

    for user_id in user_ids:

        print()

        print(f"Processing User : {user_id}")

        generate_preferences(user_id)

        preferences = get_preferences(user_id)

        print("Saved Preferences")

        print("-" * 60)

        for preference_type, value, score in preferences:

            print(
                f"{preference_type:<10}"
                f"{value:<25}"
                f"Score : {score}"
            )


if __name__ == "__main__":
    main()