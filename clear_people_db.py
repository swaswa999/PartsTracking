import sqlite3
import os

def create_connection():
    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'people.db')
    conn = sqlite3.connect(db_path)
    return conn

def clear_tables():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS parts')
    cursor.execute('DROP TABLE IF EXISTS people')
    conn.commit()
    conn.close()

def create_tables():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS people (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            mech_group TEXT NOT NULL,
            parts_done INTEGER DEFAULT 0
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS parts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER NOT NULL,
            part_name TEXT NOT NULL,
            difficulty INTEGER,
            qc_attempts INTEGER,
            machine_used TEXT,
            status TEXT DEFAULT 'In Progress',
            FOREIGN KEY (person_id) REFERENCES people (id)
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    clear_tables()
    create_tables()
    print("People database cleared and tables recreated.")