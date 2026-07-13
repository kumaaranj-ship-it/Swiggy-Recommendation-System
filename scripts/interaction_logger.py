import sqlite3
from datetime import datetime

from scripts.database import get_connection

# ==========================================
# CHECK USER EXISTS
# ==========================================

def user_exists(user_id):
    """
    Returns True if the user exists.
    """

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT 1
        FROM users
        WHERE user_id = ?
        """,
        (user_id,)
    )

    result = cursor.fetchone()

    conn.close()

    return result is not None


# ==========================================
# CHECK RESTAURANT EXISTS
# ==========================================

def restaurant_exists(restaurant_id):
    """
    Returns True if the restaurant exists.
    """

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT 1
        FROM restaurants
        WHERE restaurant_id = ?
               """,
        (restaurant_id,)
    )

    result = cursor.fetchone()

    conn.close()

    return result is not None


# ==========================================
# CURRENT DATE & TIME
# ==========================================

def current_timestamp():
    """
    Returns the current date and time.
    """

    return datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    # ==========================================
# SEARCH RESTAURANTS
# ==========================================

def search_restaurants(keyword):
    """
    Search restaurants by name, city
    or cuisine.
    """

    conn = get_connection()

    cursor = conn.cursor()

    search_text = "%" + keyword + "%"

    cursor.execute(
        """
        SELECT
            restaurant_id,
            name,
            city,
            cuisine,
            rating,
            cost
        FROM restaurants
        WHERE
            name LIKE ?
            OR city LIKE ?
            OR cuisine LIKE ?
        ORDER BY rating DESC
        """,
        (
            search_text,
            search_text,
            search_text
        )
    )

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

            "cost": row[5]

        }

        restaurants.append(
            restaurant
        )

    return restaurants


# ==========================================
# LOG SEARCH HISTORY
# ==========================================

def log_search(user_id, keyword):
    """
    Save the user's search into
    search_history.
    """

    if not user_exists(user_id):

        print("Invalid User ID.")

        return

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO search_history
        (
            user_id,
            search_query,
            search_time
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
            keyword,
            current_timestamp()
        )
    )

    conn.commit()

    conn.close()

    print("Search logged successfully.")
    
    
# ==========================================
# DISPLAY SEARCH RESULTS
# ==========================================

def display_restaurants(restaurants):
    """
    Display the list of restaurants.
    """

    if len(restaurants) == 0:

        print("\nNo restaurants found.")

        return

    print("\nMatching Restaurants")
    print("-" * 80)

    for restaurant in restaurants:

        print(f"Restaurant ID : {restaurant['restaurant_id']}")
        print(f"Name          : {restaurant['restaurant_name']}")
        print(f"City          : {restaurant['city']}")
        print(f"Cuisine       : {restaurant['cuisine']}")
        print(f"Rating        : {restaurant['rating']}")
        print(f"Cost          : ₹{restaurant['cost']}")
        print("-" * 80)


# ==========================================
# LOG CLICK HISTORY
# ==========================================

def log_click(user_id, restaurant_id):
    """
    Save a restaurant click.
    """

    if not user_exists(user_id):

        print("Invalid User ID.")

        return

    if not restaurant_exists(restaurant_id):

        print("Invalid Restaurant ID.")

        return

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO click_history
        (
            user_id,
            restaurant_id,
            click_time
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
            current_timestamp()
        )
    )

    conn.commit()

    conn.close()

    print("Restaurant click logged successfully.")
# ==========================================
# ADD TO FAVOURITES
# ==========================================

def add_to_favourites(user_id, restaurant_id):
    """
    Add a restaurant to the user's
    favourites.
    """

    if not user_exists(user_id):

        print("Invalid User ID.")

        return

    if not restaurant_exists(restaurant_id):

        print("Invalid Restaurant ID.")

        return

    conn = get_connection()

    cursor = conn.cursor()

    # -----------------------------
    # Check Existing Favourite
    # -----------------------------

    cursor.execute(
        """
        SELECT favourite_id
        FROM favourites
        WHERE
            user_id = ?
            AND restaurant_id = ?
        """,
        (
            user_id,
            restaurant_id
        )
    )

    favourite = cursor.fetchone()

    if favourite is not None:

        print("Restaurant is already in favourites.")

        conn.close()

        return

    # -----------------------------
    # Insert Favourite
    # -----------------------------

    cursor.execute(
        """
        INSERT INTO favourites
        (
            user_id,
            restaurant_id,
            added_date
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
            current_timestamp()
        )
    )

    conn.commit()

    conn.close()

    print("Restaurant added to favourites successfully.")


# ==========================================
# REMOVE FROM FAVOURITES
# ==========================================

def remove_from_favourites(user_id, restaurant_id):
    """
    Remove a restaurant from the
    user's favourites.
    """

    if not user_exists(user_id):

        print("Invalid User ID.")

        return

    if not restaurant_exists(restaurant_id):

        print("Invalid Restaurant ID.")

        return

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM favourites
        WHERE
            user_id = ?
            AND restaurant_id = ?
        """,
        (
            user_id,
            restaurant_id
        )
    )

    conn.commit()

    if cursor.rowcount == 0:

        print("Restaurant was not found in favourites.")

    else:

        print("Restaurant removed from favourites successfully.")

    conn.close()


# ==========================================
# VIEW FAVOURITES
# ==========================================

def view_favourites(user_id):
    """
    Display all favourite restaurants
    of a user.
    """

    if not user_exists(user_id):

        print("Invalid User ID.")

        return

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            r.restaurant_id,
            r.name,
            r.city,
            r.cuisine,
            r.rating,
            r.cost
        FROM favourites f
        INNER JOIN restaurants r
            ON f.restaurant_id = r.restaurant_id
        WHERE f.user_id = ?
        ORDER BY r.rating DESC
        """,
        (user_id,)
    )

    rows = cursor.fetchall()

    conn.close()

    if len(rows) == 0:

        print("\nNo favourite restaurants found.")

        return

    print("\nFavourite Restaurants")
    print("-" * 80)

    for row in rows:

        print(f"Restaurant ID : {row[0]}")
        print(f"Name          : {row[1]}")
        print(f"City          : {row[2]}")
        print(f"Cuisine       : {row[3]}")
        print(f"Rating        : {row[4]}")
        print(f"Cost          : ₹{row[5]}")
        print("-" * 80)
        # ==========================================
# ADD OR UPDATE RATING
# ==========================================

def add_rating(user_id, restaurant_id, rating):
    """
    Add or update a user's rating
    for a restaurant.
    """

    if not user_exists(user_id):

        print("Invalid User ID.")

        return

    if not restaurant_exists(restaurant_id):

        print("Invalid Restaurant ID.")

        return

    if rating < 1 or rating > 5:

        print("Rating must be between 1 and 5.")

        return

    conn = get_connection()

    cursor = conn.cursor()

    # --------------------------------------
    # Check Existing Rating
    # --------------------------------------

    cursor.execute(
        """
        SELECT rating_id
        FROM ratings
        WHERE
            user_id = ?
            AND restaurant_id = ?
        """,
        (
            user_id,
            restaurant_id
        )
    )

    existing_rating = cursor.fetchone()

    # --------------------------------------
    # Update Existing Rating
    # --------------------------------------

    if existing_rating is not None:

        cursor.execute(
            """
            UPDATE ratings
            SET
                rating = ?,
                rating_date = ?
            WHERE
                user_id = ?
                AND restaurant_id = ?
            """,
            (
                rating,
                current_timestamp(),
                user_id,
                restaurant_id
            )
        )

        print("Rating updated successfully.")

    # --------------------------------------
    # Insert New Rating
    # --------------------------------------

    else:

        cursor.execute(
            """
            INSERT INTO ratings
            (
                user_id,
                restaurant_id,
                rating,
                rating_date
            )
            VALUES
            (
                ?,
                ?,
                ?,
                ?
            )
            """,
            (
                user_id,
                restaurant_id,
                rating,
                current_timestamp()
            )
        )

        print("Rating added successfully.")

    conn.commit()

    conn.close()


# ==========================================
# VIEW USER RATINGS
# ==========================================

def view_ratings(user_id):
    """
    Display all ratings given
    by a user.
    """

    if not user_exists(user_id):

        print("Invalid User ID.")

        return

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            r.restaurant_id,
            rs.name,
            rs.city,
            rs.cuisine,
            r.rating
        FROM ratings r
        INNER JOIN restaurants rs
            ON r.restaurant_id = rs.restaurant_id
        WHERE r.user_id = ?
        ORDER BY r.rating DESC
        """,
        (user_id,)
    )

    rows = cursor.fetchall()

    conn.close()

    if len(rows) == 0:

        print("\nNo ratings found.")

        return

    print("\nYour Ratings")
    print("-" * 80)

    for row in rows:

        print(f"Restaurant ID : {row[0]}")
        print(f"Name          : {row[1]}")
        print(f"City          : {row[2]}")
        print(f"Cuisine       : {row[3]}")
        print(f"Your Rating   : {row[4]}")
        print("-" * 80)
        
        # ==========================================
# STREAMLIT COMPATIBILITY WRAPPERS
# ==========================================

def add_favourite(user_id, restaurant_id):
    """
    Wrapper for Streamlit UI.
    """
    return add_to_favourites(
        user_id,
        restaurant_id
    )


def remove_favourite(user_id, restaurant_id):
    """
    Wrapper for Streamlit UI.
    """
    return remove_from_favourites(
        user_id,
        restaurant_id
    )


def rate_restaurant(user_id, restaurant_id, rating):
    """
    Wrapper for Streamlit UI.
    """
    return add_rating(
        user_id,
        restaurant_id,
        rating
    )


def already_favourite(user_id, restaurant_id):
    """
    Returns True if the restaurant is
    already in the user's favourites.
    """

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT 1
        FROM favourites
        WHERE
            user_id = ?
            AND restaurant_id = ?
        """,
        (
            user_id,
            restaurant_id
        )
    )

    result = cursor.fetchone()

    conn.close()

    return result is not None


# ==========================================
# MAIN MENU
# ==========================================

def main():

    while True:

        print("\n" + "=" * 60)
        print("Swiggy Interaction Logger")
        print("=" * 60)

        print("1. Search Restaurants")
        print("2. Log Restaurant Click")
        print("3. Add to Favourites")
        print("4. Remove from Favourites")
        print("5. View Favourites")
        print("6. Add / Update Rating")
        print("7. View Ratings")
        print("8. Exit")

        choice = input("\nEnter your choice : ").strip()

        # --------------------------------------
        # Search Restaurants
        # --------------------------------------

        if choice == "1":

            user_input = input("Enter User ID : ").strip()

            if not user_input.isdigit():

                print("Invalid User ID.")

                continue

            user_id = int(user_input)

            keyword = input(
                "Enter restaurant name, city or cuisine : "
            ).strip()

            log_search(
                user_id,
                keyword
            )

            restaurants = search_restaurants(
                keyword
            )

            display_restaurants(
                restaurants
            )

        # --------------------------------------
        # Log Restaurant Click
        # --------------------------------------

        elif choice == "2":

            user_input = input("Enter User ID : ").strip()

            restaurant_input = input(
                "Enter Restaurant ID : "
            ).strip()

            if (
                not user_input.isdigit()
                or
                not restaurant_input.isdigit()
            ):

                print("Invalid input.")

                continue

            log_click(
                int(user_input),
                int(restaurant_input)
            )

        # --------------------------------------
        # Add Favourite
        # --------------------------------------

        elif choice == "3":

            user_input = input("Enter User ID : ").strip()

            restaurant_input = input(
                "Enter Restaurant ID : "
            ).strip()

            if (
                not user_input.isdigit()
                or
                not restaurant_input.isdigit()
            ):

                print("Invalid input.")

                continue

            add_to_favourites(
                int(user_input),
                int(restaurant_input)
            )

        # --------------------------------------
        # Remove Favourite
        # --------------------------------------

        elif choice == "4":

            user_input = input("Enter User ID : ").strip()

            restaurant_input = input(
                "Enter Restaurant ID : "
            ).strip()

            if (
                not user_input.isdigit()
                or
                not restaurant_input.isdigit()
            ):

                print("Invalid input.")

                continue

            remove_from_favourites(
                int(user_input),
                int(restaurant_input)
            )

        # --------------------------------------
        # View Favourites
        # --------------------------------------

        elif choice == "5":

            user_input = input("Enter User ID : ").strip()

            if not user_input.isdigit():

                print("Invalid User ID.")

                continue

            view_favourites(
                int(user_input)
            )

        # --------------------------------------
        # Add Rating
        # --------------------------------------

        elif choice == "6":

            user_input = input("Enter User ID : ").strip()

            restaurant_input = input(
                "Enter Restaurant ID : "
            ).strip()

            rating_input = input(
                "Enter Rating (1-5) : "
            ).strip()

            if (
                not user_input.isdigit()
                or
                not restaurant_input.isdigit()
            ):

                print("Invalid input.")

                continue

            try:

                rating = float(
                    rating_input
                )

            except ValueError:

                print("Invalid Rating.")

                continue

            add_rating(

                int(user_input),

                int(restaurant_input),

                rating

            )

        # --------------------------------------
        # View Ratings
        # --------------------------------------

        elif choice == "7":

            user_input = input("Enter User ID : ").strip()

            if not user_input.isdigit():

                print("Invalid User ID.")

                continue

            view_ratings(
                int(user_input)
            )

        # --------------------------------------
        # Exit
        # --------------------------------------

        elif choice == "8":

            print("\nThank you for using the Interaction Logger.")

            break

        else:

            print("\nInvalid Choice.")


# ==========================================
# PROGRAM ENTRY
# ==========================================

if __name__ == "__main__":

    main()