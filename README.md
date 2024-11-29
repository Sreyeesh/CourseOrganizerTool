# **Course Organizer Tool**

The **Course Organizer Tool** is a Python CLI utility designed to streamline the process of organizing and managing video content for online courses. This tool helps with tasks such as renaming videos, creating course directories with sections, moving videos into the appropriate sections, and calculating total course length.

---

## **Features**

1. **List Source Videos**:
   - Displays all videos in the source directory with their current names and sizes.
2. **Interactive Renaming**:
   - Quickly preview videos and rename them interactively using a standardized naming convention.
3. **Create Course Folders**:
   - Automatically create course directories with a specified number of sections.
4. **Move Videos to Course**:
   - Organizes videos into sections based on their names and moves them to the appropriate course folder.
5. **Calculate Course Duration**:
   - Calculates the total length of all videos in a course folder to prepare Udemy metadata.
6. **List Course Details**:
   - Displays a detailed structure of a course folder, including sections and videos.

---

## **Folder and File Structure**

### **Naming Conventions**

| **Entity**        | **Example**                                     | **Description**                                   |
|-------------------|-------------------------------------------------|-------------------------------------------------|
| **Course Folder** | `Python_CLI_Development`                        | The main folder for the course.                 |
| **Section Folder**| `Section_01_Getting_Started`                    | Each section starts with a numeric prefix.      |
| **Video File**    | `Section01_Lecture01_Introduction_to_the_Course.mp4` | Videos follow a descriptive naming pattern.     |

### **Example Folder Layout**
```
Python_CLI_Development/
├── Section_01_Getting_Started/
│   ├── Section01_Lecture01_Introduction_to_the_Course.mp4
│   ├── Section01_Lecture02_Setting_Up_Your_Environment.mp4
├── Section_02_Core_Features/
│   ├── Section02_Lecture01_Adding_Notes.mp4
│   ├── Section02_Lecture02_Listing_Notes.mp4
├── Supplementary_Materials/
│   ├── Course_Outline.pdf
│   ├── Cheatsheet.pdf
```

---

## **Available Commands**

| **Command**                       | **Description**                                                                 |
|-----------------------------------|---------------------------------------------------------------------------------|
| `list-source-videos`              | Lists all videos in the source directory with their sizes.                     |
| `quick-rename`                    | Opens videos for quick preview and renames them interactively.                 |
| `create-course`                   | Creates a new course folder with standardized section subfolders.              |
| `move-videos-to-course`           | Moves videos from the source directory into sections in the course folder.     |
| `calculate-course-length`         | Calculates the total duration of videos in a course folder.                    |
| `list-course-details`             | Lists the sections and videos in a course folder.                              |

---

## **Installation**

### **Pre-requisites**
- Python 3.8+
- FFmpeg (for calculating video durations)
  - Download [here](https://ffmpeg.org/download.html) and add it to your system's PATH.

### **Install Globally**

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/course-organizer-tool.git
   cd course-organizer-tool
   ```

2. Install the tool:
   ```bash
   pip install .
   ```

3. Verify installation:
   ```bash
   organizer --help
   ```

---

## **Usage**

### **1. List Videos in Source Directory**
Displays all videos in the source directory:
```bash
organizer list-source-videos
```

---

### **2. Rename Videos**
Preview and rename videos interactively:
```bash
organizer quick-rename
```
- **Example Workflow**:
  ```
  Current file: Recording_2024-11-29_10-00-00.mp4
  Opening video for quick preview...
  Enter Section number (e.g., 01): 1
  Enter Lecture number (e.g., 01): 1
  Enter video title (e.g., Introduction_to_the_Course): Introduction_to_the_Course
  Renamed: Recording_2024-11-29_10-00-00.mp4 -> Section01_Lecture01_Introduction_to_the_Course.mp4
  ```

---

### **3. Create a Course Folder**
Create a course folder with a specified number of sections:
```bash
organizer create-course "Python_CLI_Development" --sections 7
```

---

### **4. Move Videos to a Course Folder**
Moves renamed videos into their respective sections in the course folder:
```bash
organizer move-videos-to-course "Python_CLI_Development"
```

---

### **5. List Course Details**
Displays the structure of a course folder:
```bash
organizer list-course-details "Python_CLI_Development"
```

---

### **6. Calculate Course Duration**
Calculates the total duration of all videos in a course folder:
```bash
organizer calculate-course-length "Python_CLI_Development"
```

---

## **Workflow**

1. **Record Videos**:
   - Save recordings in the `SOURCE_DIR` (e.g., `C:\Users\sgari\Videos\Videos`).

2. **Rename Videos**:
   - Use `quick-rename` to assign descriptive names based on the course outline.

3. **Create Course Folder**:
   - Run `create-course` to set up the course directory and sections.

4. **Move Videos**:
   - Use `move-videos-to-course` to organize videos into the correct sections.

5. **Verify Course Folder**:
   - Use `list-course-details` to inspect the organized structure.

6. **Calculate Duration**:
   - Use `calculate-course-length` to get the total course length for Udemy metadata.

---

## **License**
This tool is open-source and licensed under the MIT License.

---

## **Contributing**
Feel free to submit issues or pull requests to enhance the tool’s functionality.

---

## **Support**
For any issues, contact **Sreyeesh Garimella**.

---

Let me know if you need further adjustments or additional sections! 😊