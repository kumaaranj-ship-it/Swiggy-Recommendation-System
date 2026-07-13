import sqlite3

from scripts.database import get_connection

conn = sqlite3.connect("database/swiggy.db")
cursor = conn.cursor()

cursor.execute("""
SELECT
    user_id,
    preference_type,
    preference_value,
    score
FROM user_preferences
ORDER BY user_id, preference_type
""")

rows = cursor.fetchall()

print(f"Total Preference Records : {len(rows)}")
print()

for row in rows:
    print(row)

conn.close()