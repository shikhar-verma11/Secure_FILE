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

def login(username, password):
    """Authenticate user by verifying hashed password."""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT password_hash, role FROM users WHERE username = ?', (username,))
    result = cursor.fetchone()
    conn.close()

    if result and result[0] == hash_password(password):
        print(f'Login successful! Role: {result[1]}')
        return result[1]
    else:
        print('Invalid username or password.')
        return None


def get_user_role(username):
    """Retrieve the role of a user."""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT role FROM users WHERE username = ?', (username,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None
