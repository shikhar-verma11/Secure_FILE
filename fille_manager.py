import os

def get_user_folder(username):
    folder_path = os.path.join("secure_files", username)
    os.makedirs(folder_path, exist_ok=True)
    return folder_path

