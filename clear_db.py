import sqlite3
import os

def create_connection():
    db_path = os.path.join(os.path.dirname(__file__), 'data', 'parts.db')
    print(f"Database path: {db_path}")  # Debugging: Print the database path
    conn = sqlite3.connect(db_path)
    return conn

def clear_table():
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM parts')
        conn.commit()
        conn.close()
        print("Database cleared.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    clear_table()