---

# Course Organizer CLI

The **Course Organizer CLI** is a Python-based tool designed to help you organize and manage video files for Udemy courses. It includes functionality for calculating the total length of video files, organizing them into structured course folders, and generating metadata files with course information.

---

## Prerequisites

1. **Python**: Ensure Python is installed (version 3.6 or later).
2. **moviepy**: Install the `moviepy` library, which is used for calculating video durations.
   ```bash
   pip install moviepy
   ```
3. **Configuration File**: Make sure you have a `config.yaml` file in the same directory with the following structure:

   ```yaml
   # config.yaml

   base_course_path: "C:/Users/sgari/Documents/UdemyCourses"
   obs_video_path: "C:/Users/sgari/Videos/Videos"
   course_prefix: "TOUCAN_COURSE"
   starting_course_number: 1
   sections_per_course: 7
   lectures_per_section: 2
   file_extension: ".mp4"
   ```

---

## Commands

### 1. `calculate-total-video-length`

**Description**:  
This command calculates and displays the total duration of all videos in each `TOUCAN_COURSE_###` folder located within the `base_course_path`. It also generates a metadata file in each course folder containing the course name and total length of videos.

**Usage**:  
```bash
python course_organizer.py calculate-total-video-length
```

**Output**:
- For each course folder (`TOUCAN_COURSE_###`), a `{course_name}_metadata.txt` file is generated, containing:
  - Course Name
  - Total Length of all videos in `hh:mm:ss` format.

**Example Output**:
```plaintext
TOUCAN_COURSE_001 - Total duration of videos: 2h 30m 45s
Metadata saved to: C:/Users/sgari/Documents/UdemyCourses/TOUCAN_COURSE_001/TOUCAN_COURSE_001_metadata.txt
```

### 2. `organize-videos`

**Description**:  
This command organizes videos from the `obs_video_path` into structured folders under the next available `TOUCAN_COURSE_###` course folder. Videos are renamed to match the format `SectionXX_LectureXX.mp4` and are moved into corresponding section folders like `Section_01`, `Section_02`, etc.

**Usage**:  
```bash
python course_organizer.py organize-videos
```

**How It Works**:
1. Checks the `base_course_path` for the next available course number (e.g., if `TOUCAN_COURSE_001` and `TOUCAN_COURSE_002` exist, it creates `TOUCAN_COURSE_003`).
2. Creates section folders (`Section_01`, `Section_02`, etc.) within the course folder.
3. Renames and moves each video from `obs_video_path` into the appropriate section folder, following the naming convention `SectionXX_LectureXX.mp4`.

**Example**:
- Before: `C:/Users/sgari/Videos/Videos/video1.mp4`
- After: `C:/Users/sgari/Documents/UdemyCourses/TOUCAN_COURSE_003/Section_01/Section01_Lecture01.mp4`

---

## Additional Information

- **Logging**: All actions, including renaming and moving files, are logged in `course_organizer.log`.
- **Course Naming and Structure**:
  - Each new course is automatically numbered (e.g., `TOUCAN_COURSE_001`, `TOUCAN_COURSE_002`, etc.) based on existing folders in `base_course_path`.
  - The `config.yaml` file controls the course structure, including the number of sections and lectures per section.

---

## Example Workflow

1. **Calculate Total Video Length**:
   ```bash
   python course_organizer.py calculate-total-video-length
   ```

2. **Organize Videos**:
   ```bash
   python course_organizer.py organize-videos
   ```

Use these commands to manage and prepare your video files for Udemy courses efficiently.

---
