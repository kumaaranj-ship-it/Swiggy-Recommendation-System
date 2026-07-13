from pathlib import Path
import hashlib

from scripts.database import get_connection


# =========================================
# CURRENT USER SESSION
# =========================================

current_user = None


# =========================================
# PASSWORD HASHING
# =========================================

def hash_password(password):
    """
    Convert a plain text password into a SHA-256 hash.
    """
    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


# =========================================
# CHECK USERNAME EXISTS
# =========================================

def username_exists(username):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT 1
        FROM users
        WHERE username = ?
        """,
        (username,)
    )

    exists = cursor.fetchone() is not None

    connection.close()

    return exists


# =========================================
# CHECK EMAIL EXISTS
# =========================================

def email_exists(email):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT 1
        FROM users
        WHERE email = ?
        """,
        (email,)
    )

    exists = cursor.fetchone() is not None

    connection.close()

    return exists


# =========================================
# REGISTER USER
# =========================================

def register_user(
    username,
    email,
    password
):

    if username_exists(username):
        return False, "Username already exists."

    if email_exists(email):
        return False, "Email already exists."

    hashed_password = hash_password(password)

    connection = get_connection()
    cursor = connection.cursor()

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
            hashed_password
        )
    )

    connection.commit()

    connection.close()

    return True, "Registration successful."


# =========================================
# LOGIN USER
# =========================================

def login_user(
    username,
    password
):

    global current_user

    hashed_password = hash_password(password)

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            user_id,
            username,
            email
        FROM users
        WHERE
            username = ?
        AND
            password = ?
        """,
        (
            username,
            hashed_password
        )
    )

    user = cursor.fetchone()

    connection.close()

    if user is None:
        return False, "Invalid username or password."

    current_user = {
        "user_id": user[0],
        "username": user[1],
        "email": user[2]
    }

    return True, "Login successful."


# =========================================
# LOGOUT USER
# =========================================

def logout_user():

    global current_user

    current_user = None


# =========================================
# GET CURRENT USER
# =========================================

def get_current_user():

    return current_user


# =========================================
# TEST MODULE
# =========================================

if __name__ == "__main__":

    print("\nTesting User Authentication\n")

    status, message = register_user(
        username="kumaaran",
        email="kumaaran@test.com",
        password="admin123"
    )

    print(message)

    status, message = login_user(
        username="kumaaran",
        password="admin123"
    )

    print(message)

    print("\nCurrent User")

    print(get_current_user())

    logout_user()

    print("\nAfter Logout")

    print(get_current_user())