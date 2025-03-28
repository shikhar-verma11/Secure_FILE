import os
from auth import register, login
from security import encrypt_and_store, decrypt_and_read, encrypt_file, decrypt_file
from file_manager import delete_file

def list_user_files(username):
    folder_path = os.path.join("secure_files", username)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    return [f[:-4] for f in os.listdir(folder_path) if f.endswith(".enc")]

def update_file(username):
    files = list_user_files(username)
    if not files:
        print("No files available to update.")
        return
    print("Your Encrypted Files:")
    for idx, file in enumerate(files, 1):
        print(f"{idx}. {file}")

    try:
        index = int(input("Enter file number to update: ")) - 1
    except ValueError:
        print("Enter a valid number.")
        return

    if not (0 <= index < len(files)):
        print("Invalid selection.")
        return

    enc_file_path = os.path.join("secure_files", username, files[index] + ".enc")
    decrypt_file(enc_file_path)
    decrypted_path = enc_file_path.replace(".enc", "")

    with open(decrypted_path, "r") as f:
        current_content = f.read()

    print("Current content:")
    print(current_content)

    new_content = input("Enter new content: ")

    with open(decrypted_path, "w") as f:
        f.write(new_content)

    encrypt_file(decrypted_path)
    print(f"File '{files[index]}' updated.")

def delete_selected_file(username):
    files = list_user_files(username)
    if not files:
        print("No files available to delete.")
        return
    print("Your Files:")
    for i, f in enumerate(files, 1):
        print(f"{i}. {f}")
    try:
        index = int(input("Enter file number to delete: ")) - 1
    except ValueError:
        print("Enter a valid number.")
        return
    if not (0 <= index < len(files)):
        print("Invalid selection.")
        return
    filename = files[index] + ".enc"
    delete_file(username, filename)
    print(f"File '{filename}' deleted.")

def user_dashboard(username):
    while True:
        print(f"\nSecure File Dashboard for {username}")
        print("1. Create & Encrypt a New File")
        print("2. View & Decrypt Existing Files")
        print("3. Update a File")
        print("4. Delete a File")
        print("5. List Files")
        print("6. Logout")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            file_name = input("Enter new file name (with .txt extension): ").strip()
            folder_path = os.path.join("secure_files", username)
            os.makedirs(folder_path, exist_ok=True)
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, "w") as f:
                content = input("Enter file content: ")
                f.write(content)
            encrypt_and_store(username, file_name)
            print(f"File '{file_name}' created and encrypted.")
        elif choice == "2":
            files = list_user_files(username)
            if not files:
                print("No files found.")
                continue
            print("Your Encrypted Files:")
            for idx, file in enumerate(files, 1):
                print(f"{idx}. {file}")
            try:
                index = int(input("Enter file number to open: ")) - 1
                if 0 <= index < len(files):
                    decrypt_and_read(username, files[index])
                else:
                    print("Invalid selection.")
            except ValueError:
                print("Enter a valid number.")
        elif choice == "3":
            update_file(username)
        elif choice == "4":
            delete_selected_file(username)
        elif choice == "5":
            files = list_user_files(username)
            print("Your Files:")
            for file in files:
                print(file)
        elif choice == "6":
            print("Logging out...")
            break
        else:
            print("Invalid option.")

def main():
    os.makedirs("secure_files", exist_ok=True)
    while True:
        print("\nSecure File Management System")
        print("1. Register User")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            username = input("Enter username: ").strip()
            password = input("Enter password: ").strip()
            register(username, password)
        elif choice == "2":
            username = input("Enter username: ").strip()
            password = input("Enter password: ").strip()
            role = login(username, password)
            if role:
                user_dashboard(username)
        elif choice == "3":
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
