import sqlite3
import os

def create_connection():
    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'people.db')
    conn = sqlite3.connect(db_path)
    return conn

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

def add_person(name, mech_group):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO people (name, mech_group)
        VALUES (?, ?)
    ''', (name, mech_group))
    conn.commit()
    conn.close()

def add_part(person_id, part_name, difficulty, qc_attempts, machine_used, status='In Progress'):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO parts (person_id, part_name, difficulty, qc_attempts, machine_used, status)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (person_id, part_name, difficulty, qc_attempts, machine_used, status))
    conn.commit()
    conn.close()

def get_person_id(name):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM people WHERE name = ?', (name,))
    person_id = cursor.fetchone()
    conn.close()
    return person_id[0] if person_id else None

def get_all_people():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM people')
    people = cursor.fetchall()
    conn.close()
    return people

def get_person_by_id(person_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM people WHERE id = ?', (person_id,))
    person = cursor.fetchone()
    conn.close()
    return person

def get_parts_by_person(person_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM parts WHERE person_id = ?', (person_id,))
    parts = cursor.fetchall()
    conn.close()
    return parts

def initialize_data():
    data = {
        "Pivot": ["Michi", "Nitzan", "Caroline", "Ruby", "Jacob", "Hannah", "Anna", "Ava", "Tom", "Meni", "Satvik"],
        "Alae Intake  (4th)": ["Antonio","Victor", "Jesse", "Erin", "Stella", "Brandon", "Johnny", "Nadia", "Fabi", "Hamza", "Misha"],
        "Elevator": ["Kaavya","Lucca", "Tony", "Keiss", "Alvin", "Justin", "Ethan", "Andrew", "Sophie", "Parker"],
        "Climb": ["David", "Riya", "Swayam", "Siyona", "Holden", "Samuel", "Avanti", "Sangeet", "Tanmay", "Bani"],
    }
    for mech_group, people in data.items():
        for person in people:
            add_person(person, mech_group)

if __name__ == '__main__':
    create_tables()
    initialize_data()
    print("Database initialized with people data.")