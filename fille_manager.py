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
