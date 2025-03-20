import sqlite3

def query_users():
    conn = sqlite3.connect('app/development.db')
    cursor = conn.cursor()

    print("Users in the database:")
    cursor.execute("SELECT id, email, first_name, last_name, is_admin FROM user")
    rows = cursor.fetchall()
    for row in rows:
        print(f"ID: {row[0]}, Email: {row[1]}, Name: {row[2]} {row[3]}, Admin: {row[4]}")

    conn.close()

def query_places():
    conn = sqlite3.connect('app/development.db')
    cursor = conn.cursor()

    print("\nPlaces in the database:")
    cursor.execute("SELECT id, name, description, user_id FROM place")
    rows = cursor.fetchall()
    for row in rows:
        print(f"ID: {row[0]}, Name: {row[1]}, User ID: {row[3]}")

    conn.close()

def query_reviews():
    conn = sqlite3.connect('app/development.db')
    cursor = conn.cursor()

    print("\nReviews in the database:")
    cursor.execute("SELECT id, text, place_id, user_id FROM review")
    rows = cursor.fetchall()
    for row in rows:
        print(f"ID: {row[0]}, Place ID: {row[2]}, User ID: {row[3]}")

    conn.close()

def query_amenities():
    conn = sqlite3.connect('app/development.db')
    cursor = conn.cursor()

    print("\nAmenities in the database:")
    cursor.execute("SELECT id, name FROM amenity")
    rows = cursor.fetchall()
    for row in rows:
        print(f"ID: {row[0]}, Name: {row[1]}")

    conn.close()

if __name__ == "__main__":
    query_users()
    query_places()
    query_reviews()
    query_amenities() 
