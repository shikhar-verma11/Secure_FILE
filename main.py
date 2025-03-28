from auth import register, login
from file_manager import create_file, read_file, update_file, delete_file, list_user_files
from security import encrypt_and_store, decrypt_and_read

def main():
    print("🔐 Secure File Management System")
    
    while True:
        print("\n1️⃣ Register User\n2️⃣ Login\n3️⃣ Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            username = input("Enter username: ")
            password = input("Enter password: ")
            register(username, password)
        elif choice == "2":
            username = input("Enter username: ")
            password = input("Enter password: ")
            role = login(username, password)
            
            if role:
                user_dashboard(username)
        elif choice == "3":
            print("👋 Exiting...")
            break
        else:
            print("❌ Invalid choice.")

def user_dashboard(username):
    while True:
        print(f"\n📂 Welcome, {username}!")
        print("\n1️⃣ Create File\n2️⃣ Read File\n3️⃣ Update File\n4️⃣ Delete File\n5️⃣ List Files\n6️⃣ Logout")
        choice = input("Choose an option: ")

        if choice == "1":
            file_name = input("Enter file name: ")
            content = input("Enter file content: ")
            create_file(username, file_name, content)
            encrypt_and_store(username, file_name)
        elif choice == "2":
            file_name = input("Enter file name to read: ")
            decrypt_and_read(username, file_name)
        elif choice == "3":
            file_name = input("Enter file name to update: ")
            update_file(username, file_name)
        elif choice == "4":
            file_name = input("Enter file name to delete: ")
            delete_file(username, file_name)
        elif choice == "5":
            list_user_files(username)
        elif choice == "6":
            print("🔒 Logging out...")
            break
        else:
            print("❌ Invalid choice.")

if __name__ == "__main__":
    main()
