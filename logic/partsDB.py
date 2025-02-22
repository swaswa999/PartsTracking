import sqlite3
import os

def create_connection():
    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'parts.db')
    conn = sqlite3.connect(db_path)
    return conn

def create_tables():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS parts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            photo TEXT,
            description TEXT,
            priority INTEGER,
            number_of_parts INTEGER,
            machine_type TEXT,
            difficulty INTEGER,
            tolerance TEXT,
            assigned_machinist TEXT,
            drawing_sheet_creator TEXT,
            mech_type TEXT,
            progress TEXT DEFAULT 'Awaiting_Approval',
            qc_attempts INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

def add_part(part):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO parts (
            name, photo, description, priority, number_of_parts, machine_type,
            difficulty, tolerance, assigned_machinist, drawing_sheet_creator,
            mech_type, progress, qc_attempts
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        part['name'], part['photo'], part['description'], part['priority'],
        part['number_of_parts'], part['machine_type'], part['difficulty'],
        part['tolerance'], part['assigned_machinist'],
        part['drawing_sheet_creator'], part['mech_type'], part['progress'],
        part['qc_attempts']
    ))
    conn.commit()
    conn.close()

def get_all_parts():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM parts')
    parts = cursor.fetchall()
    conn.close()
    return parts

def get_part_by_id(part_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM parts WHERE id = ?', (part_id,))
    part = cursor.fetchone()
    conn.close()
    return part

def update_part(part_id, updated_part):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE parts
        SET
            name = ?,
            photo = ?,
            description = ?,
            priority = ?,
            number_of_parts = ?,
            machine_type = ?,
            difficulty = ?,
            tolerance = ?,
            assigned_machinist = ?,
            drawing_sheet_creator = ?,
            mech_type = ?,
            progress = ?,
            qc_attempts = ?
        WHERE id = ?
    ''', (
        updated_part['name'], updated_part['photo'], updated_part['description'],
        updated_part['priority'], updated_part['number_of_parts'],
        updated_part['machine_type'], updated_part['difficulty'],
        updated_part['tolerance'], updated_part['assigned_machinist'],
        updated_part['drawing_sheet_creator'], updated_part['mech_type'],
        updated_part['progress'], updated_part['qc_attempts'], part_id
    ))
    conn.commit()
    conn.close()

def get_parts_by_person(person_name):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM parts WHERE assigned_machinist = ?', (person_name,))
    parts = cursor.fetchall()
    conn.close()
    return parts

def get_parts_by_status(status):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM parts WHERE progress = ?', (status,))
    parts = cursor.fetchall()
    conn.close()
    return parts

# Create the table when the module is imported
create_tables()