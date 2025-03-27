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

import hashlib

def hash_password(password):
    """Generate SHA256 hash for the password."""
    return hashlib.sha256(password.encode()).hexdigest()

def register(username, password, role='user'):
    """Register a new user with a hashed password."""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)',
                       (username, hash_password(password), role))
        conn.commit()
        print(f'User "{username}" registered successfully as "{role}".')
    except sqlite3.IntegrityError:
        print(f'Username "{username}" already exists.')
    conn.close()
