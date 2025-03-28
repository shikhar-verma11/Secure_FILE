import os

def get_user_folder(username):
    """Create and return the folder path for a user."""
    folder_path = os.path.join("secure_files", username)
    os.makedirs(folder_path, exist_ok=True)
    return folder_path


def create_file(username, file_name, content):
    """Create a file and write content."""
    folder_path = get_user_folder(username)
    file_path = os.path.join(folder_path, file_name)

    with open(file_path, "w") as f:
        f.write(content)

    print(f"✅ File '{file_name}' created for user '{username}'.")


def read_file(username, file_name):
    """Read a file's content and return it."""
    folder_path = get_user_folder(username)
    file_path = os.path.join(folder_path, file_name)

    if not os.path.exists(file_path):
        print(f"❌ Error: File '{file_name}' not found.")
        return None

    with open(file_path, "r") as f:
        content = f.read()

    return content


def update_file(username, file_name, new_content):
    """Update the content of an existing file."""
    folder_path = get_user_folder(username)
    file_path = os.path.join(folder_path, file_name)

    if not os.path.exists(file_path):
        print(f"❌ Error: File '{file_name}' not found.")
        return

    with open(file_path, "w") as f:
        f.write(new_content)

    print(f"✅ File '{file_name}' updated successfully.")


def delete_file(username, file_name):
    """Delete a file."""
    folder_path = get_user_folder(username)
    file_path = os.path.join(folder_path, file_name)

    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"🗑️ File '{file_name}' deleted.")
    else:
        print(f"❌ Error: File '{file_name}' not found.")


def list_user_files(username):
    """List all files of a user and return them."""
    folder_path = get_user_folder(username)

    if not os.path.exists(folder_path):
        print(f"❌ User '{username}' has no files.")
        return []

    files = os.listdir(folder_path)

    if not files:
        print(f"📂 No files found for user '{username}'.")
    else:
        print(f"📂 Files for user '{username}':")
        for file in files:
            print(f"- {file}")

    return files


# CLI testing (optional)
if __name__ == "__main__":
    print("🔐 Secure File Manager (CLI Mode)")
    while True:
        print("\n1. Create File\n2. Read File\n3. Update File\n4. Delete File\n5. List Files\n6. Exit")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            username = input("Enter username: ")
            file_name = input("Enter file name: ")
            content = input("Enter file content: ")
            create_file(username, file_name, content)

        elif choice == "2":
            username = input("Enter username: ")
            file_name = input("Enter file name: ")
            content = read_file(username, file_name)
            if content is not None:
                print(f"\n📖 Content of '{file_name}':\n{content}\n")

        elif choice == "3":
            username = input("Enter username: ")
            file_name = input("Enter file name: ")
            new_content = input("Enter new content: ")
            update_file(username, file_name, new_content)

        elif choice == "4":
            username = input("Enter username: ")
            file_name = input("Enter file name: ")
            delete_file(username, file_name)

        elif choice == "5":
            username = input("Enter username: ")
            list_user_files(username)

        elif choice == "6":
            print("👋 Exiting...")
            break
