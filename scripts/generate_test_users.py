# ==========================================
# Generate Dummy Users
# ==========================================
#
# This script generates dummy users
# and interaction history for testing
# the Hybrid Recommendation System.
#
# ==========================================

import random
import string
try:
    from scripts.database import get_connection
    from scripts.user_auth import hash_password
except ModuleNotFoundError:
    from database import get_connection
    from user_auth import hash_password
# ==========================================
# Database Location
# ==========================================

DATABASE = "database/swiggy.db"

# ==========================================
# Load Restaurant IDs
# ==========================================

def load_restaurant_ids():
    """
    Load all restaurant IDs
    from the database.
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT restaurant_id
        FROM restaurants
        """
    )

    rows = cursor.fetchall()

    connection.close()

    restaurant_ids = []

    for row in rows:

        restaurant_ids.append(row[0])

    return restaurant_ids


# ==========================================
# Generate Username
# ==========================================

def generate_username(user_number):
    """
    Generate a unique username.
    """

    return f"test_user_{user_number}"


# ==========================================
# Generate Password
# ==========================================

def generate_password(length=8):
    """
    Generate a random password.
    """

    characters = (
        string.ascii_letters +
        string.digits
    )

    password = ""

    for _ in range(length):

        password += random.choice(characters)

    return password
# ==========================================
# Create Dummy Users
# ==========================================

def create_dummy_users(number_of_users=10):
    """
    Create dummy users in the users table.
    """

    connection = get_connection()

    cursor = connection.cursor()

    created_users = []

    for user_number in range(1, number_of_users + 1):

        username = generate_username(user_number)

        email = f"{username}@example.com"

        password = generate_password()

        # ----------------------------------
        # Check Existing Username
        # ----------------------------------

        cursor.execute(
            """
            SELECT user_id
            FROM users
            WHERE username = ?
            """,
            (username,)
        )

        existing_user = cursor.fetchone()

        if existing_user is not None:

            print(
                f"Skipped : {username} (Already Exists)"
            )

            continue

        # ----------------------------------
        # Insert New User
        # ----------------------------------

        cursor.execute(
            """
            INSERT INTO users
            (
                username,
                email,
                password
            )
            VALUES
            (
                ?,
                ?,
                ?
            )
            """,
            (
                username,
                email,
                hash_password(password)
            )
        )

        created_users.append(username)

        print(
            f"Created : {username} | Password : {password}"
        )

    connection.commit()

    connection.close()

    return created_users

# ==========================================
# Load User IDs
# ==========================================

def load_user_ids():
    """
    Load all user IDs except the
    original user (User ID = 1).
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT user_id
        FROM users
        WHERE user_id > 1
        """
    )

    rows = cursor.fetchall()

    connection.close()

    user_ids = []

    for row in rows:

        user_ids.append(row[0])

    return user_ids


# ==========================================
# Load Restaurant Names
# ==========================================

def load_restaurant_names():
    """
    Load all restaurant names.
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT name
        FROM restaurants
        """
    )

    rows = cursor.fetchall()

    connection.close()

    restaurant_names = []

    for row in rows:

        restaurant_names.append(row[0])

    return restaurant_names


# ==========================================
# Generate Search History
# ==========================================

def generate_search_history(
    searches_per_user=15
):
    """
    Generate random search history
    for every dummy user.
    """

    user_ids = load_user_ids()

    restaurant_names = load_restaurant_names()

    connection = get_connection()

    cursor = connection.cursor()

    total_searches = 0

    for user_id in user_ids:

        random_restaurants = random.sample(
            restaurant_names,
            searches_per_user
        )

        for restaurant_name in random_restaurants:

            cursor.execute(
                """
                INSERT INTO search_history
                (
                    user_id,
                    search_query
                )
                VALUES
                (
                    ?,
                    ?
                )
                """,
                (
                    user_id,
                    restaurant_name
                )
            )

            total_searches += 1

    connection.commit()

    connection.close()

    print()

    print(
        f"Generated {total_searches} search records."
    )
    
    # ==========================================
# Generate Click History
# ==========================================

def generate_click_history(
    clicks_per_user=10
):
    """
    Generate random click history
    for every dummy user.
    """

    user_ids = load_user_ids()

    restaurant_ids = load_restaurant_ids()

    connection = get_connection()

    cursor = connection.cursor()

    total_clicks = 0

    for user_id in user_ids:

        random_restaurants = random.sample(
            restaurant_ids,
            clicks_per_user
        )

        for restaurant_id in random_restaurants:

            cursor.execute(
                """
                INSERT INTO click_history
                (
                    user_id,
                    restaurant_id
                )
                VALUES
                (
                    ?,
                    ?
                )
                """,
                (
                    user_id,
                    restaurant_id
                )
            )

            total_clicks += 1

    connection.commit()

    connection.close()

    print()

    print(
        f"Generated {total_clicks} click records."
    )
    # ==========================================
# Generate Favourite Restaurants
# ==========================================

def generate_favourites(
    favourites_per_user=5
):
    """
    Generate random favourite restaurants
    for every dummy user.
    """

    user_ids = load_user_ids()

    restaurant_ids = load_restaurant_ids()

    connection = get_connection()

    cursor = connection.cursor()

    total_favourites = 0

    for user_id in user_ids:

        random_restaurants = random.sample(
            restaurant_ids,
            favourites_per_user
        )

        for restaurant_id in random_restaurants:

            # ----------------------------------
            # Avoid Duplicate Favourites
            # ----------------------------------

            cursor.execute(
                """
                SELECT favourite_id
                FROM favourites
                WHERE user_id = ?
                AND restaurant_id = ?
                """,
                (
                    user_id,
                    restaurant_id
                )
            )

            existing = cursor.fetchone()

            if existing is not None:
                continue

            # ----------------------------------
            # Insert Favourite
            # ----------------------------------

            cursor.execute(
                """
                INSERT INTO favourites
                (
                    user_id,
                    restaurant_id
                )
                VALUES
                (
                    ?,
                    ?
                )
                """,
                (
                    user_id,
                    restaurant_id
                )
            )

            total_favourites += 1

    connection.commit()

    connection.close()

    print()

    print(
        f"Generated {total_favourites} favourite records."
    )
    # ==========================================
# Generate Ratings
# ==========================================

def generate_ratings(
    ratings_per_user=8
):
    """
    Generate random restaurant ratings
    for every dummy user.
    """

    user_ids = load_user_ids()

    restaurant_ids = load_restaurant_ids()

    connection = get_connection()

    cursor = connection.cursor()

    total_ratings = 0

    for user_id in user_ids:

        random_restaurants = random.sample(
            restaurant_ids,
            ratings_per_user
        )

        for restaurant_id in random_restaurants:

            # ----------------------------------
            # Skip Existing Ratings
            # ----------------------------------

            cursor.execute(
                """
                SELECT rating_id
                FROM ratings
                WHERE user_id = ?
                AND restaurant_id = ?
                """,
                (
                    user_id,
                    restaurant_id
                )
            )

            existing_rating = cursor.fetchone()

            if existing_rating is not None:
                continue

            # ----------------------------------
            # Generate Random Rating
            # ----------------------------------

            rating = round(
                random.uniform(3.0, 5.0),
                1
            )

            # ----------------------------------
            # Insert Rating
            # ----------------------------------

            cursor.execute(
                """
                INSERT INTO ratings
                (
                    user_id,
                    restaurant_id,
                    rating
                )
                VALUES
                (
                    ?,
                    ?,
                    ?
                )
                """,
                (
                    user_id,
                    restaurant_id,
                    rating
                )
            )

            total_ratings += 1

    connection.commit()

    connection.close()

    print()

    print(
        f"Generated {total_ratings} rating records."
    )
    # ==========================================
# Main Function
# ==========================================

def main():
    """
    Execute the complete dummy
    data generation pipeline.
    """

    print("=" * 50)
    print("Generate Dummy Users")
    print("=" * 50)

    # ----------------------------------
    # Create Dummy Users
    # ----------------------------------

    users = create_dummy_users(10)

    print()

    print(
        f"Total New Users Created : {len(users)}"
    )

    # ----------------------------------
    # Generate Search History
    # ----------------------------------

    generate_search_history()

    # ----------------------------------
    # Generate Click History
    # ----------------------------------

    generate_click_history()

    # ----------------------------------
    # Generate Favourite History
    # ----------------------------------

    generate_favourites()

    # ----------------------------------
    # Generate Ratings
    # ----------------------------------

    generate_ratings()

    print()

    print("=" * 50)
    print("Dummy Data Generation Completed")
    print("=" * 50)


# ==========================================
# Program Entry
# ==========================================

if __name__ == "__main__":
    main()