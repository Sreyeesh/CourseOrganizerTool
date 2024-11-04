
---

# Course Organizer Tool

This tool helps organize and rename video files for Udemy course creation. It creates a course folder structure based on a predefined outline, moves videos from a source directory, and renames them according to the course structure.

## Table of Contents
1. [Setup](#setup)
2. [Configuration Files](#configuration-files)
3. [Workflow](#workflow)
4. [Commands](#commands)
5. [Examples](#examples)

---

## Setup

1. Clone or download this repository.
2. Ensure you have Python installed (version 3.6 or higher recommended).
3. Install any required dependencies (if needed).
4. Place your video files in the designated `obs_video_path` folder, as defined in `config.yaml`.

---

## Configuration Files

This tool relies on two configuration files:

### 1. `config.yaml`
Defines the paths where the course and videos are stored. Update the paths to match your environment.

```yaml
base_course_path: "C:/Users/sgari/Documents/UdemyCourses"  # Folder to create the course structure
obs_video_path: "C:/Users/sgari/Videos/Videos"             # Folder where OBS saves recorded videos
```

### 2. `course_outline.yaml`
Defines the course structure with the course acronym and sections, each containing lecture titles.

```yaml
course_acronym: "PyCLI_Docker"
sections:
  "01_Overview":
    - "01_Course_Introduction"
    - "02_Objectives"
  "02_Project_Structure":
    - "01_Folder_Setup"
    - "02_Essential_Files"
  "03_Docker_Environment":
    - "01_Docker_Installation"
    - "02_Writing_Dockerfile"
    - "03_VS_Code_Setup"
```

> **Note**: Use the exact format shown to ensure proper section and lecture folder creation.

---

## Workflow

### 1. Configure the Project
   - Update `config.yaml` with the correct paths for your course base directory and OBS video save directory.
   - Edit `course_outline.yaml` to define the course acronym, sections, and lectures.

### 2. Create the Course Folder Structure
   - Run the command to create folders for each section and lecture based on `course_outline.yaml`.

### 3. Organize and Rename Videos
   - Place your recorded videos in the folder specified in `obs_video_path`.
   - Run the `organize-videos-cmd` command to move and rename the videos according to the course structure.

### 4. (Optional) Rename Existing Videos
   - If needed, use the `rename-videos-cmd` to ensure videos are named according to the lecture titles.

---

## Commands

### 1. Create the Course Structure

Creates the folder structure based on `course_outline.yaml`.

```bash
python course_organizer.py create-structure
```

- **Expected Output**: Creates a folder structure at `base_course_path/course_acronym`.

### 2. Organize Videos into the Course Structure

Moves videos from `obs_video_path` to the course structure, renaming them based on `course_outline.yaml`.

```bash
python course_organizer.py organize-videos-cmd
```

- **Expected Output**: Moves and renames videos into the appropriate folders and titles within the course structure.

### 3. Rename Videos in the Course Structure (Optional)

Ensures videos in the course structure are renamed based on `course_outline.yaml`.

```bash
python course_organizer.py rename-videos-cmd
```

- **Expected Output**: Renames any existing videos within the course structure to match the lecture titles.

---

## Examples

1. **Create Course Structure**:
   ```bash
   python course_organizer.py create-structure
   ```
   **Description**: Creates folders for each section and lecture in `C:/Users/sgari/Documents/UdemyCourses/PyCLI_Docker`.

2. **Organize Videos**:
   ```bash
   python course_organizer.py organize-videos-cmd
   ```
   **Description**: Moves and renames videos from `C:/Users/sgari/Videos/Videos` into the course folder, following the sequence in `course_outline.yaml`.

3. **Rename Videos (Optional)**:
   ```bash
   python course_organizer.py rename-videos-cmd
   ```
   **Description**: Ensures video names in the course structure match the titles in `course_outline.yaml`.

---
