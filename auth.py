# auth.py
import sqlite3

def initialize_db():
    """Initialize the user database."""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        password_hash TEXT,
                        role TEXT DEFAULT 'user')''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_db()
