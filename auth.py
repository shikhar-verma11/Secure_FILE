import sqlite3
import hashlib
import pyotp
import qrcode

DB_NAME = "secure_file_manager.db"

def initialize_db():
    """Initialize the user database with 2FA support."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        password_hash TEXT,
                        role TEXT DEFAULT 'user',
                        totp_secret TEXT)''')
    conn.commit()
    conn.close()

initialize_db()

def hash_password(password):
    """Generate SHA256 hash for the password."""
    return hashlib.sha256(password.encode()).hexdigest()

def validate_username(username):
    """Check if the username meets minimum requirements."""
    return len(username) >= 3

def validate_password(password):
    """Ensure password meets security standards."""
    return len(password) >= 6

def register(username, password, role='user'):
    """Register a user and generate a unique 2FA secret key."""
    if not validate_username(username):
        print("❌ Username must be at least 3 characters long.")
        return
    if not validate_password(password):
        print("❌ Password must be at least 6 characters long.")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    secret = pyotp.random_base32() 
    try:
        cursor.execute(
            'INSERT INTO users (username, password_hash, role, totp_secret) VALUES (?, ?, ?, ?)',
            (username, hash_password(password), role, secret)
        )
        conn.commit()
        print(f'✅ User "{username}" registered successfully!')

        totp = pyotp.TOTP(secret)
        uri = totp.provisioning_uri(username, issuer_name="SecureFileManager")

        print("\n📲 Scan this QR code in Google Authenticator or Authy:\n")
        qr = qrcode.make(uri)
        qr.show()

    except sqlite3.IntegrityError:
        print(f'❌ Username "{username}" already exists.')
    finally:
        conn.close()

def login(username, password):
    """Authenticate user with password and 2FA."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT password_hash, role, totp_secret FROM users WHERE username = ?', (username,))
    result = cursor.fetchone()
    conn.close()

    if result and result[0] == hash_password(password):
        totp_secret = result[2]
        totp = pyotp.TOTP(totp_secret)
        otp = input("🔑 Enter 2FA Code from Authenticator App: ").strip()

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
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT role FROM users WHERE username = ?', (username,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def list_users():
    """List all registered users (Admin only)."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT username, role FROM users')
    users = cursor.fetchall()
    conn.close()

    print("\n📋 Registered Users:")
    if users:
        for user, role in users:
            print(f"  - {user} ({role})")
    else:
        print("No users found.")

def reset_2fa(username):
    """Reset 2FA secret for a user."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    new_secret = pyotp.random_base32()
    cursor.execute('UPDATE users SET totp_secret = ? WHERE username = ?', (new_secret, username))
    conn.commit()
    conn.close()

    print(f'🔄 2FA reset for "{username}". Scan the new QR code in your Authenticator app.')

    totp = pyotp.TOTP(new_secret)
    uri = totp.provisioning_uri(username, issuer_name="SecureFileManager")

    qr = qrcode.make(uri)
    qr.show()

if __name__ == "__main__":
    while True:
        print("\n1. Register\n2. Login\n3. List Users (Admin Only)\n4. Reset 2FA\n5. Exit")
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
            username = input("Enter username to reset 2FA: ")
            reset_2fa(username)
        elif choice == '5':
            break
        else:
            print("❌ Invalid choice. Please try again.")

# === STREAMLIT-COMPATIBLE FUNCTIONS ===

def register_user(username, password):
    """Register a user for Streamlit and return (success, message, secret or None)"""
    if not validate_username(username):
        return False, "Username must be at least 3 characters long.", None
    if not validate_password(password):
        return False, "Password must be at least 6 characters long.", None

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    secret = pyotp.random_base32()

    try:
        cursor.execute(
            'INSERT INTO users (username, password_hash, role, totp_secret) VALUES (?, ?, ?, ?)',
            (username, hash_password(password), 'user', secret)
        )
        conn.commit()
        return True, "User registered successfully.", secret
    except sqlite3.IntegrityError:
        return False, "Username already exists.", None
    finally:
        conn.close()


def login_user(username, password):
    """Login function for Streamlit. Returns (success, role or message, secret)"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT password_hash, role, totp_secret FROM users WHERE username = ?', (username,))
    result = cursor.fetchone()
    conn.close()

    if result and result[0] == hash_password(password):
        return True, result[1], result[2]  # (success, role, secret)
    else:
        return False, "Invalid credentials", None


def verify_2fa_code(secret, otp):
    """Verify the TOTP 2FA code for Streamlit."""
    totp = pyotp.TOTP(secret)
    return totp.verify(otp)

def get_user_secret(username):
    """Retrieve the TOTP secret for a given user."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT totp_secret FROM users WHERE username = ?', (username,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

