
---

# **Course Organizer**

The **Course Organizer** is a Python CLI tool designed for renaming, organizing, and managing video files for Udemy-style course creation. It ensures that videos are structured properly into course folders with section-specific subfolders.

---

## **Project Structure**

```
course_organizer/
    ├── course_organizer/
    │   ├── __init__.py          # Initializes the course organizer module
    │   ├── organizer.py         # Main script for organizing and managing videos
    ├── course_organizer.egg-info/
    │   ├── ...                  # Metadata for package distribution
    ├── venv/                    # Virtual environment for dependencies
    ├── .gitattributes           # Git attributes configuration
    ├── .gitignore               # Files and folders to ignore in version control
    ├── README.md                # Documentation for the project
    ├── requirements.txt         # List of dependencies
    ├── setup.py                 # Script for packaging and installing the module
```

---

## **Features**

1. **Automatic Course Folder Creation**:
   - Dynamically assigns videos to the next available course folder (e.g., `TOUCAN_COURSE_001`).

2. **Section Subfolder Organization**:
   - Automatically creates subfolders (`Section_01`, `Section_02`, etc.) within the course folder for better structure.

3. **Custom Video Renaming**:
   - Renames videos with a consistent format based on the course name, section, and timestamp.

4. **Preview Mode**:
   - Allows you to preview the renaming and organization process without making changes.

5. **Video Sorting**:
   - Ensures videos are processed in chronological order using their modification times.

6. **Duration Calculation**:
   - Calculates the total length of all videos in the source directory.

---

## **Dependencies**

Ensure you have the following installed:

- Python 3.6 or later
- `ffmpeg` for calculating video duration (installable via [ffmpeg.org](https://ffmpeg.org/download.html))
- Python packages:
  ```bash
  pip install -r requirements.txt
  ```

---

## **Installation**

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/course-organizer.git
   cd course-organizer
   ```

2. Set up the virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/macOS
   venv\Scripts\activate      # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Ensure `ffmpeg` is installed and added to your system PATH.

---

## **Usage**

### **Commands**

#### **1. Organize Videos**
Organizes videos into dynamically determined course folders with section subfolders.

```bash
python -m course_organizer.organizer organize-videos "CourseName"
```

**Example**:
```bash
python -m course_organizer.organizer organize-videos "BuildingCLIApp"
```

This will rename and move videos into the next available course folder (`TOUCAN_COURSE_001`, etc.) with subfolders for each section.

---

#### **2. Preview Organization**
Preview the renaming and organization process without making changes:

```bash
python -m course_organizer.organizer organize-videos "CourseName" --preview
```

---

#### **3. Calculate Total Video Length**
Calculate the total duration of all videos in the source directory:

```bash
python -m course_organizer.organizer calculate-total-length
```

---

## **Directory Structure After Organization**

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
    ├── TOUCAN_COURSE_001
    │   ├── Section_01
    │   │   ├── BuildingCLIApp_S01_20241126_140621.mp4
    │   │   ├── ...
    │   ├── Section_02
    │   │   ├── BuildingCLIApp_S02_20241126_144558.mp4
    │   │   ├── ...
```

---

## **Development**

1. To add new features or modify functionality, edit `organizer.py` in the `course_organizer` folder.
2. Test your changes using the preview mode:
   ```bash
   python -m course_organizer.organizer organize-videos "YourCourse" --preview
   ```

---

## **Contributing**

Contributions are welcome! If you have suggestions or find issues, feel free to open an issue or submit a pull request.

---

## **License**

This project is licensed under the MIT License. See the LICENSE file for details.

---

