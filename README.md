Here's a **README** file for your `Course Organizer Tool` project. This README includes setup instructions, usage examples, and explanations of each command.

---

# Course Organizer Tool

The **Course Organizer Tool** is a command-line Python script that helps organize course materials into a structured folder hierarchy based on metadata such as `provider`, `category`, `course_name`, `section`, and `lecture`. This tool moves and renames files according to a standardized naming convention, making it easy to keep your course materials organized and accessible.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Examples](#examples)
- [Folder Structure](#folder-structure)

## Features
- **Organize Course Files**: Organizes files by moving them into a structured folder hierarchy.
- **Standardized Naming Convention**: Renames files using a consistent format for easy identification.
- **Flexible Configuration**: Customizable root folder, recording directory, and default filename through a configuration file.
- **Supports Multiple Courses**: Organizes files into separate folders by category, course, section, and lecture.

## Installation
1. Clone this repository or download the script.
2. Ensure you have Python 3 installed.

## Configuration
The tool uses a `config.yaml` file to define paths and categories. Place this file in the same directory as the script.

### Example `config.yaml`
```yaml
settings:
  # Root folder where organized courses will be saved
  root_folder: "C:\\Users\\sgari\\Documents\\UdemyCourses"
  
  # Static list of categories for course organization
  categories:
    - "Python"
    - "DevOps"
    - "GameDevelopment"

paths:
  # Path to the directory where video recordings are stored
  recording_directory: "C:\\Users\\sgari\\Videos\\Videos"
  
  # Default filename for organize command if only a filename is specified
  default_filename: "lecture1.mp4"
```

- **`root_folder`**: The main directory where all organized courses will be stored.
- **`categories`**: A list of predefined categories.
- **`recording_directory`**: Directory where raw video files are initially saved.
- **`default_filename`**: Default file to use if `--filename` is not specified.

## Usage
Run the script using Python with the following syntax:

```bash
python course_organizer.py <action> [options]
```

### Actions
1. **`setup_folders`**: Initializes the folder structure based on `config.yaml`.
2. **`organize`**: Moves and renames a single file from the `recording_directory` to the organized folder structure.
3. **`organize_from_recording`**: Moves and renames all files in the `recording_directory` based on specified parameters.

### Options
- `--provider`: Provider name (e.g., `udemy`).
- `--category`: Category of the course (e.g., `Python`, `DevOps`).
- `--course_name`: Name of the course.
- `--section`: Section name or number.
- `--lecture`: Lecture name or number.
- `--filename` (optional): Name of the file to organize, defaults to `default_filename` if omitted.

## Examples

### 1. Set Up Folder Structure
Initializes the folder structure under `root_folder`, with subfolders for each category specified in `config.yaml`.

```bash
python course_organizer.py setup_folders
```

### 2. Organize a Specific File by Section and Lecture
Moves and renames a single file from `recording_directory` to the organized folder structure based on `provider`, `category`, `course_name`, `section`, and `lecture`.

```bash
python course_organizer.py organize --provider "udemy" --category "Python" --course_name "intro_to_python" --section "section1" --lecture "lecture1" --filename "lecture2.mp4"
```

**Explanation**:
- Finds `lecture2.mp4` in `recording_directory`.
- Renames it to a standardized filename like `udemy_python_intro_to_python_section1_lecture1_11_06_2024.mp4`.
- Moves it to `root_folder/category/course_name/section`.

### 3. Organize All Files in `recording_directory`
Moves and renames all files from the `recording_directory` to the specified course structure.

```bash
python course_organizer.py organize_from_recording --provider "udemy" --category "DevOps" --course_name "learning_devops" --section "section2" --lecture "lecture3"
```

## Folder Structure
The script organizes files into a hierarchy under `root_folder` with a standardized naming convention. Here’s an example structure after organizing a course:

```
UdemyCourses/
├── Python/
│   ├── intro_to_python/
│   │   ├── section1/
│   │   │   ├── udemy_python_intro_to_python_section1_lecture1_11_06_2024.mp4
│   │   └── section2/
│   │       └── udemy_python_intro_to_python_section2_lecture3_11_06_2024.mp4
├── DevOps/
│   ├── learning_devops/
│   │   ├── section1/
│   │   └── section2/
└── GameDevelopment/
```

## Notes
- **Ensure Filenames are Unique**: The script appends a timestamp to help maintain unique filenames.
- **Configuration**: Modify paths or categories in `config.yaml` to fit your setup.
- **Error Handling**: If a file is missing or incorrectly specified, the script will notify you and skip the operation.

---

This README provides a comprehensive guide for setting up and using the Course Organizer Tool. Let me know if you'd like any additional information or examples included!