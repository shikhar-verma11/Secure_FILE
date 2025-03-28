import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

KEY_FILE = "encryption_key.key"

def generate_key():
    if not os.path.exists(KEY_FILE):
        key = get_random_bytes(32)  # 256-bit AES key
        with open(KEY_FILE, "wb") as f:
            f.write(key)
        print("🔑 Encryption key generated.")
    else:
        print("🔑 Encryption key already exists.")

def load_key():
    generate_key()  # Ensure key exists before loading
    with open(KEY_FILE, "rb") as f:
        return f.read()


generate_key()


def encrypt_file(file_path):
    """Encrypt a file using AES encryption."""
    key = load_key()
    cipher = AES.new(key, AES.MODE_EAX)

    with open(file_path, "rb") as f:
        plaintext = f.read()

    ciphertext, tag = cipher.encrypt_and_digest(plaintext)

    with open(file_path + ".enc", "wb") as f:
        f.write(cipher.nonce + tag + ciphertext)

    os.remove(file_path)  # Remove the original file
    print(f"🔒 File '{file_path}' encrypted successfully.")

def decrypt_file(file_path):
    """Decrypt a file encrypted with AES."""
    key = load_key()

    with open(file_path, "rb") as f:
        nonce = f.read(16)
        tag = f.read(16)
        ciphertext = f.read()

    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)

    original_path = file_path.replace(".enc", "")
    with open(original_path, "wb") as f:
        f.write(plaintext)

    os.remove(file_path)  # Remove the encrypted file
    print(f"🔓 File '{original_path}' decrypted successfully.")

def ensure_enc_extension(file_name):
    """Ensure the file has the .enc extension."""
    if not file_name.endswith(".enc"):
        file_name += ".enc"
    return file_name

def encrypt_and_store(username, file_name):
    """Encrypt a file and store it securely."""
    folder_path = os.path.join("secure_files", username)
    file_path = os.path.join(folder_path, file_name)

    if os.path.exists(file_path):
        encrypt_file(file_path)
    else:
        print(f"❌ Error: '{file_name}' not found for user '{username}'.")

def decrypt_and_read(username, file_name):
    """Decrypt a file and read its content."""
    folder_path = os.path.join("secure_files", username)
    enc_file_path = os.path.join(folder_path, ensure_enc_extension(file_name))

    if os.path.exists(enc_file_path):
        decrypt_file(enc_file_path)
        decrypted_path = enc_file_path.replace(".enc", "")

        with open(decrypted_path, "r") as f:
            content = f.read()
            print(f"\n📖 Content of '{file_name}':\n{content}\n")

        encrypt_file(decrypted_path)  # Re-encrypt after reading
    else:
        print(f"❌ Error: '{file_name}' not found.")

if __name__ == "__main__":
    print("🔐 Secure Encryption Module Loaded.")