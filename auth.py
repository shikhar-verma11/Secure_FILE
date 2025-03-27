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
    """Authenticate user with password and 2FA."""
    conn = sqlite3.connect('secure_file_manager.db')
    cursor = conn.cursor()
    cursor.execute('SELECT password_hash, role, totp_secret FROM users WHERE username = ?', (username,))
    result = cursor.fetchone()
    conn.close()

    if result and result[0] == hash_password(password):
        totp_secret = result[2]
        totp = pyotp.TOTP(totp_secret)
        otp = input("Enter 2FA Code from Authenticator App: ").strip()

        if totp.verify(otp):
            print(f'✅ Login successful! Role: {result[1]}')
            return result[1]  # Return user role ('admin' or 'user')
        else:
            print('❌ Invalid 2FA code.')
            return None
    else:
        print('❌ Invalid username or password.')
        return None

def get_user_role(username):
    """Retrieve the role of a user."""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT role FROM users WHERE username = ?', (username,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None


def list_users():
    """List all registered users (Admin only)."""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT username, role FROM users')
    users = cursor.fetchall()
    conn.close()

    print("\nRegistered Users:")
    for user, role in users:
        print(f"- {user} ({role})")

def validate_username(username):
    """Check if the username meets requirements."""
    return len(username) >= 3

def validate_password(password):
    """Ensure password meets security standards."""
    return len(password) >= 6


if __name__ == "__main__":
    initialize_db()
    while True:
        print("\n1. Register\n2. Login\n3. List Users (Admin Only)\n4. Exit")
        choice = input("Enter choice: ").strip()
        if choice == '1':
            username = input("Enter username: ")
            password = input("Enter password: ")
            register(username, password)
        elif choice == '2':
            username = input("Enter username: ")
            password = input("Enter password: ")
            login(username, password)
        elif choice == '3':
            list_users()
        elif choice == '4':
            break

import pyotp

def register(username, password, role='user'):
    """Register a user and generate a unique 2FA secret key."""
    conn = sqlite3.connect('secure_file_manager.db')
    cursor = conn.cursor()

    secret = pyotp.random_base32()  # Generate unique 2FA key
    try:
        cursor.execute(
            'INSERT INTO users (username, password_hash, role, totp_secret) VALUES (?, ?, ?, ?)',
            (username, hash_password(password), role, secret)
        )
        conn.commit()
        print(f'✅ User "{username}" registered successfully!')

        # Generate QR Code for 2FA setup
        totp = pyotp.TOTP(secret)
        uri = totp.provisioning_uri(username, issuer_name="SecureFileManager")

        print("\n📲 Scan this QR code in Google Authenticator or Authy:\n")
        import qrcode
        qr = qrcode.make(uri)
        qr.show()

    except sqlite3.IntegrityError:
        print(f'❌ Username "{username}" already exists.')
    finally:
        conn.close()
