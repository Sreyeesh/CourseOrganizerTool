### **Updated README**

---

# **TOUCAN Video Organizer**

The TOUCAN Video Organizer is a Python CLI tool for organizing videos into structured course folders. It automatically renames and moves videos into section-specific subfolders for easy management and course creation.

---

## **Features**

1. **Automatic Course Folder Creation**:
   - Dynamically assigns videos to the next available course folder (e.g., `TOUCAN_COURSE_005`).

2. **Section Subfolder Organization**:
   - Automatically creates subfolders (`Section_01`, `Section_02`, etc.) for each course.

3. **Custom Video Renaming**:
   - Renames videos with a consistent format based on the course name, section, and timestamp.

4. **Video Sorting**:
   - Ensures videos are processed in chronological order using their modification times.

5. **Duration Calculation**:
   - Calculates the total length of all videos in the source directory.

6. **Preview Mode**:
   - Allows you to preview changes before applying them.

---

## **Dependencies**

Ensure you have the following installed:
- Python 3.6 or later
- `ffprobe` (part of the `ffmpeg` package) for calculating video duration
- Python packages:
  ```bash
  pip install click tqdm
  ```

---

## **Installation**

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/TOUCAN-Video-Organizer.git
   cd TOUCAN-Video-Organizer
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure the `ffmpeg` package is installed:
   - [Download ffmpeg](https://ffmpeg.org/download.html) and add it to your system's PATH.

---

## **Usage**

### **Commands**

### 1. **Organize Videos**
Organizes videos into a dynamically determined course folder with section subfolders.

**Command**:
```bash
python organizer.py organize-videos "CourseName"
```

**Example**:
```bash
python organizer.py organize-videos "BuildingCLIApp"
```

**Result**:
- Videos in the source directory will be renamed and moved into the next available course folder (e.g., `TOUCAN_COURSE_005`) with subfolders like:
  ```
  TOUCAN_COURSE_005
      ├── Section_01
      │   ├── BuildingCLIApp_S01_20241126_140621.mp4
      │   ├── ...
      ├── Section_02
      │   ├── BuildingCLIApp_S02_20241126_144558.mp4
      │   ├── ...
  ```

---

### 2. **Preview Organization**
Preview how videos will be renamed and organized before making changes.

**Command**:
```bash
python organizer.py organize-videos "CourseName" --preview
```

---

### 3. **Calculate Total Video Length**
Calculates the total duration of all videos in the source directory.

**Command**:
```bash
python organizer.py calculate-total-length
```

**Result**:
- Displays the total duration in minutes and seconds.

---

### **Directory Structure**

Before running the script:
```
SOURCE_DIR
    ├── Video_1.mp4
    ├── Video_2.mp4
    ├── ...
```

After running the script:
```
TARGET_DIR
    ├── TOUCAN_COURSE_005
    │   ├── Section_01
    │   │   ├── CourseName_S01_20241126_140621.mp4
    │   │   ├── ...
    │   ├── Section_02
    │   │   ├── CourseName_S02_20241126_144558.mp4
    │   │   ├── ...
```

---

## **Examples**

### Organize Videos
```bash
python organizer.py organize-videos "MyAwesomeCourse"
```

**Output**:
```
Renaming 35 videos into sections...
Assigning 'Video_1.mp4' -> Section 01
Assigning 'Video_2.mp4' -> Section 01
...
Moving videos to TOUCAN_COURSE_005...
```

---

## **Development**

### **Extending the Script**
To add additional features or modify the existing logic:
1. Open the `organizer.py` file.
2. Modify the relevant functions or commands.
3. Test changes using the preview mode:
   ```bash
   python organizer.py organize-videos "YourCourse" --preview
   ```

---

## **Contributing**

Contributions are welcome! Please open an issue or submit a pull request with suggested changes.

---

## **License**

This project is licensed under the MIT License. See the LICENSE file for details.