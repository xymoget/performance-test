# database.py

import sqlite3
from datetime import datetime

DATABASE_NAME = 'database.db'

def create_table():
    """Create the tests table if it does not exist."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS test_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            test_type TEXT,
            result INTEGER,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_test_result(test_type, result):
    """Insert a new test result into the database."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
        INSERT INTO test_results (test_type, result, timestamp)
        VALUES (?, ?, ?)
    ''', (test_type, result, timestamp))
    conn.commit()
    conn.close()

def get_test_results():
    """Retrieve all test results from the database."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT test_type, result, timestamp FROM test_results ORDER BY timestamp DESC')
    results = cursor.fetchall()
    conn.close()
    return results

# Initialize the database
create_table()
