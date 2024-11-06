import os
import yaml
import argparse
from datetime import datetime

# Configuration file path
CONFIG_FILE = "config.yaml"

# Load configuration from YAML file
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            return yaml.safe_load(file)
    return {
        "settings": {
            "root_folder": "C:\\Users\\sgari\\Documents\\UdemyCourses",
            "categories": ["Python", "DevOps", "GameDevelopment"]
        },
        "paths": {
            "recording_directory": "C:\\Users\\sgari\\Videos\\Videos",
            "default_filename": "lecture1.mp4"
        }
    }

# Save configuration to YAML file
def save_config(config):
    with open(CONFIG_FILE, "w") as file:
        yaml.dump(config, file)

# Sanitize names for filenames and folders
def sanitize_name(name):
    return name.replace(" ", "_").lower()

# Generate standardized filename
def generate_filename(provider, category, course_name, section, lecture, extension):
    timestamp = datetime.now().strftime("%m_%d_%Y")
    return f"{provider}_{sanitize_name(category)}_{sanitize_name(course_name)}_{sanitize_name(section)}_{sanitize_name(lecture)}_{timestamp}{extension}"

# Create folder structure based on categories and courses
def create_folder_structure(root_folder, categories):
    if not os.path.exists(root_folder):
        os.mkdir(root_folder)
    for category in categories:
        os.makedirs(os.path.join(root_folder, category), exist_ok=True)
    for status in ["Incomplete", "Completed"]:
        os.makedirs(os.path.join(root_folder, status), exist_ok=True)

# Organize a single file by renaming and moving it to the correct course/section/lecture folder
def organize_file(filename, provider, category, course_name, section, lecture, root_folder, recording_directory):
    filepath = os.path.join(recording_directory, filename)
    if not os.path.exists(filepath):
        print(f"File {filepath} does not exist.")
        return
    
    extension = os.path.splitext(filepath)[1]
    new_filename = generate_filename(provider, category, course_name, section, lecture, extension)
    
    # Define target folder structure and ensure folders exist
    category_folder = os.path.join(root_folder, category)
    course_folder = os.path.join(category_folder, course_name)
    section_folder = os.path.join(course_folder, section)
    os.makedirs(section_folder, exist_ok=True)

    # Move and rename the file
    new_filepath = os.path.join(section_folder, new_filename)
    os.rename(filepath, new_filepath)
    print(f"Moved and renamed {filepath} to {new_filepath}")

# Organize all video files from the recording directory based on conventions for multiple courses
def organize_files_from_recording_directory(provider, category, course_name, section, lecture):
    config = load_config()
    recording_directory = config["paths"]["recording_directory"]
    root_folder = config["settings"]["root_folder"]

    if not os.path.exists(recording_directory):
        print(f"Recording directory {recording_directory} does not exist.")
        return

    # Process each file in the recording directory
    for filename in os.listdir(recording_directory):
        filepath = os.path.join(recording_directory, filename)
        if os.path.isfile(filepath):
            extension = os.path.splitext(filepath)[1]
            new_filename = generate_filename(provider, category, course_name, section, lecture, extension)

            # Define target folder structure and ensure folders exist
            category_folder = os.path.join(root_folder, category)
            course_folder = os.path.join(category_folder, course_name)
            section_folder = os.path.join(course_folder, section)
            os.makedirs(section_folder, exist_ok=True)

            # Move and rename the file
            new_filepath = os.path.join(section_folder, new_filename)
            os.rename(filepath, new_filepath)
            print(f"Moved and renamed {filepath} to {new_filepath}")

# Main function to handle CLI arguments and execute actions
def main():
    parser = argparse.ArgumentParser(description="Course Organizer Tool with Dynamic YAML Configuration")
    parser.add_argument("action", choices=["setup_folders", "organize", "organize_from_recording"], help="Action to perform")
    parser.add_argument("--provider", help="Provider name, e.g., 'udemy'", default="udemy")
    parser.add_argument("--category", choices=["Python", "DevOps", "GameDevelopment"], help="Category of the course")
    parser.add_argument("--course_name", help="Name of the course")
    parser.add_argument("--section", help="Section name or number")
    parser.add_argument("--lecture", help="Lecture name or number")
    parser.add_argument("--filename", help="Name of the file to organize (default is set in config.yaml)")

    args = parser.parse_args()
    config = load_config()
    root_folder = config["settings"]["root_folder"]
    recording_directory = config["paths"]["recording_directory"]
    filename = args.filename if args.filename else config["paths"]["default_filename"]

    if args.action == "setup_folders":
        create_folder_structure(root_folder, config["settings"]["categories"])
        print("Folder structure created.")

    elif args.action == "organize_from_recording" and args.category and args.course_name and args.section and args.lecture:
        organize_files_from_recording_directory(args.provider, args.category, args.course_name, args.section, args.lecture)

    elif args.action == "organize" and args.category and args.course_name and args.section and args.lecture:
        organize_file(filename, args.provider, args.category, args.course_name, args.section, args.lecture, root_folder, recording_directory)
    
    else:
        print("Invalid command or missing arguments")

if __name__ == "__main__":
    main()
