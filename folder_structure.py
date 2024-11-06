# organizer/folder_structure.py
import os

def create_folder_structure(root_folder, categories):
    """Create main folder structure based on categories."""
    if not os.path.exists(root_folder):
        os.mkdir(root_folder)
    for category in categories:
        os.makedirs(os.path.join(root_folder, category), exist_ok=True)
    for status in ["Incomplete", "Completed"]:
        os.makedirs(os.path.join(root_folder, status), exist_ok=True)
