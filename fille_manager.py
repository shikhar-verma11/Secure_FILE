import os

def get_user_folder(username):
    """Create and return the folder path for a user."""
    folder_path = os.path.join("secure_files", username)
    os.makedirs(folder_path, exist_ok=True)
    return folder_path

if _name_ == "_main_":
    print("File management system initialized.")

def create_file(username, file_name, content):
    """Create a file and write content."""
    folder_path = get_user_folder(username)
    file_path = os.path.join(folder_path, file_name)

    with open(file_path, "w") as f:
        f.write(content)

    print(f"✅ File '{file_name}' created for user '{username}'.")
def read_file(username, file_name):
    """Read a file's content."""
    folder_path = get_user_folder(username)
    file_path = os.path.join(folder_path, file_name)

    if not os.path.exists(file_path):
        print(f"❌ Error: File '{file_name}' not found.")
        return

    with open(file_path, "r") as f:
        content = f.read()

    print(f"\n📖 Content of '{file_name}':\n{content}\n")
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
        print(f"🗑 File '{file_name}' deleted.")
    else:
        print(f"❌ Error: File '{file_name}' not found.")

