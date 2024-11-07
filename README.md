# Course Organizer Tool

This tool automates the process of organizing, renaming, and moving videos for a course, creating a structured folder setup and consistent naming convention for course materials.

## Features

1. **Setup Check**: Ensures paths specified in the configuration file are accessible.
2. **Create Course Folders**: Creates a course folder with numbered section subfolders.
3. **Rename Videos**: Lists and renames videos in the **videos path** (OBS video folder) to a sequential format (`SectionXX_LectureYY`).
4. **Move Videos**: Moves the renamed videos into the corresponding section folders in the main course directory.

## Requirements

- Python 3.x
- `PyYAML` package for YAML configuration:
  
  ```bash
  pip install pyyaml
  ```

## Setup Instructions

### Step 1: Configure `config.yaml`

Create a `config.yaml` file in the same directory as the script. Define the following paths and options:

```yaml
# config.yaml
base_course_path: "C:/Users/sgari/Documents/UdemyCourses"
obs_video_path: "C:/Users/sgari/Videos/Videos"
course_prefix: "TOUCAN_COURSE"
starting_course_number: 1
sections_per_course: 10
lectures_per_section: 5
```

**Configuration Options**:
- `base_course_path`: Path where course folders will be created.
- `obs_video_path`: Path to the folder containing the videos to be organized and renamed.
- `course_prefix`: Prefix for naming courses.
- `starting_course_number`: Starting number for course naming (e.g., `TOUCAN_COURSE_001`).
- `sections_per_course`: Number of sections to create per course.
- `lectures_per_section`: Number of lectures per section.

## Usage

### 1. Setup Check

Run this command to verify that all paths are configured correctly.

```bash
python course_organizer.py setup-check
```

### 2. Create Course Folder and Section Subfolders

This command creates the main course folder and section subfolders based on the specified course name.

```bash
python course_organizer.py create-course "COURSE_NAME"
```

Example:

```bash
python course_organizer.py create-course "TOUCAN_COURSE_001"
```

### 3. Rename Videos in the Videos Path

This command renames all videos in the specified **videos path** (e.g., `C:\Users\sgari\Videos\Videos`) in sequential order, starting from `Section01_Lecture01`.

```bash
python course_organizer.py rename-videos
```

### 4. Move Renamed Videos to Course Section Folders

After renaming the videos, use this command to move them into the appropriate section folders in the course directory.

```bash
python course_organizer.py move-videos "COURSE_NAME"
```

Example:

```bash
python course_organizer.py move-videos "TOUCAN_COURSE_001"
```

---

## Example Workflow

1. **Run `create-course`**: Creates `TOUCAN_COURSE_001` with sections `Section01` to `Section10` in the specified base path.

   ```bash
   python course_organizer.py create-course "TOUCAN_COURSE_001"
   ```

2. **Run `rename-videos`**: Renames all videos in the videos path (OBS video folder) to `SectionXX_LectureYY` format based on modification date.

   ```bash
   python course_organizer.py rename-videos
   ```

3. **Run `move-videos`**: Moves the renamed videos to their corresponding section folders in `TOUCAN_COURSE_001`.

   ```bash
   python course_organizer.py move-videos "TOUCAN_COURSE_001"
   ```

This structured workflow ensures that your course videos are named and organized correctly for easy access and consistent formatting.

## Notes

- Ensure that `config.yaml` is correctly set up before running any commands.
- The renaming command uses the order of modification date to rename videos sequentially.
- The script assumes that each section will contain the specified number of lectures (`lectures_per_section` in `config.yaml`). Adjust this if needed.

---

## Troubleshooting

- **No Videos Found**: Verify that the videos are in the specified `obs_video_path`.
- **Path Errors**: Ensure all paths in `config.yaml` are correct and accessible.
- **Unintended Renaming/Moving**: Run `setup-check` to verify paths, and ensure no conflicting files are present in `obs_video_path`.

---
