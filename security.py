from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os

KEY_FILE = "encryption_key.key"

def generate_key():
    """Generate and save a new encryption key."""
    if not os.path.exists(KEY_FILE):
        key = get_random_bytes(32)  # 256-bit key
        with open(KEY_FILE, "wb") as f:
            f.write(key)
        print("🔑 Encryption key generated.")
    else:
        print("🔑 Key already exists.")

if _name_ == "_main_":
    generate_key()
def load_key():
    """Load the encryption key from file."""
    if not os.path.exists(KEY_FILE):
        raise FileNotFoundError("❌ Encryption key not found. Run generate_key() first.")
    with open(KEY_FILE, "rb") as f:
        return f.read()
