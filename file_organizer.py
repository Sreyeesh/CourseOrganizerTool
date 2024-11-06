# organizer/file_organizer.py
import os
from .naming_convention import generate_filename

def organize_file(filepath, provider, category, course_name, module, purpose, root_folder):
    """Rename and move file based on conventions."""
    if not os.path.exists(filepath):
        print(f"File {filepath} does not exist.")
        return
    
    extension = os.path.splitext(filepath)[1]
    new_filename = generate_filename(provider, category, course_name, module, purpose, extension)
    
    # Define target folder and ensure it exists
    category_folder = os.path.join(root_folder, category)
    module_folder = os.path.join(category_folder, module)
    os.makedirs(module_folder, exist_ok=True)
    
    # Move and rename the file
    new_filepath = os.path.join(module_folder, new_filename)
    os.rename(filepath, new_filepath)
    print(f"Moved and renamed {filepath} to {new_filepath}")
