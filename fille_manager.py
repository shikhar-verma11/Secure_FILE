import os

def get_user_folder(username):
    """Create and return the folder path for a user."""
    folder_path = os.path.join("secure_files", username)
    os.makedirs(folder_path, exist_ok=True)
    return folder_path

if _name_ == "_main_":
    print("File management system initialized.")

