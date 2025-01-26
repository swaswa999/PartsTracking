import sqlite3
import os

def create_connection():
    db_path = os.path.join(os.path.dirname(__file__), '../../data/parts.db')
    conn = sqlite3.connect(db_path)
    return conn

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS parts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            photo TEXT NOT NULL,
            description TEXT,
            priority INTEGER,
            number_of_parts INTEGER,
            machine_type TEXT,
            difficulty TEXT,
            tolerance TEXT,
            assigned_machinist TEXT,
            drawing_sheet_creator TEXT,
            mech_type TEXT,
            progress INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def add_part(part):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO parts (name, photo, description, priority, number_of_parts, machine_type, difficulty, tolerance, assigned_machinist, drawing_sheet_creator, mech_type, progress)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (part['name'], part['photo'], part['description'], part['priority'], part['number_of_parts'], part['machine_type'], part['difficulty'], part['tolerance'], part['assigned_machinist'], part['drawing_sheet_creator'], part['mech_type'], part['progress']))
    conn.commit()
    conn.close()

def get_all_parts():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM parts')
    parts = cursor.fetchall()
    conn.close()
    return parts

# Create the table when the module is imported
create_table()