### README for Course Organizer Tool

---

# **Course Organizer Tool**

A Python-based CLI tool to organize and manage videos for Udemy courses. This tool automates the process of creating course directories, managing video files, and calculating video durations, making it easier to maintain an organized course structure.

---

## **Features**

- **Create Courses**: Generate course directories with 7 sections.
- **Generate Test Videos**: Create placeholder videos for testing purposes.
- **Move Videos**: Automatically distribute videos into appropriate sections.
- **Rename Videos**: Rename videos in the source directory for clarity.
- **List Contents**: View videos in the source directory or within a course.
- **Calculate Video Length**: Calculate the total duration of videos in the source directory.

---

## **Installation**

### **Prerequisites**

- Python 3.7 or higher
- `ffmpeg` installed and available in your system's PATH

### **Install Requirements**
Clone or download the repository and navigate to the directory. Then, install the required Python dependencies:

```bash
pip install -r requirements.txt
```

Verify `ffmpeg` is installed by running:
```bash
ffmpeg -version
```

---

## **Usage**

The script provides multiple commands to manage videos and courses. Below are the available commands:

### **1. Create a New Course**
Create a course directory with 7 sections.

```bash
python organizer.py create-course <course_number>
```

- **Example**:
  ```bash
  python organizer.py create-course 1
  ```
  Creates a directory named `TOUCAN_COURSE_001` with sections:
  ```
  Section_01, Section_02, ..., Section_07
  ```

- **Auto Increment**:
  If `<course_number>` is omitted, the next available course number will be assigned:
  ```bash
  python organizer.py create-course
  ```

---

### **2. Generate Test Videos**
Generate placeholder test videos in the source directory (`C:\Users\sgari\Videos\Videos`) for testing purposes.

```bash
python organizer.py create-test-videos <num_videos> --duration <seconds>
```

- **Example**:
  ```bash
  python organizer.py create-test-videos 5 --duration 10
  ```
  Creates 5 test videos, each 10 seconds long, with names like:
  ```
  Test_Video_01.mp4, Test_Video_02.mp4, ..., Test_Video_05.mp4
  ```

---

### **3. List Videos in the Source Directory**
View the list of videos currently in the source directory.

```bash
python organizer.py list-source-videos
```

- **Example Output**:
  ```
  Videos in source directory:
    - Test_Video_01.mp4
    - Test_Video_02.mp4
  ```

---

### **4. Rename a Video**
Rename a video in the source directory to a more meaningful name.

```bash
python organizer.py rename-video-command <old_name> <new_name>
```

- **Example**:
  ```bash
  python organizer.py rename-video-command "Test_Video_01.mp4" "Introduction_to_Python.mp4"
  ```

---

### **5. Move Videos to a Course**
Move named videos from the source directory into the appropriate sections of a course.

```bash
python organizer.py move-named-videos <course_number>
```

- **Example**:
  ```bash
  python organizer.py move-named-videos 1
  ```
  Moves videos to `TOUCAN_COURSE_001`:
  - Videos are distributed into sections (`Section_01`, `Section_02`, ...) in order.
  - Each section holds up to 5 videos.

---

### **6. List Course Contents**
View the sections and videos within a specific course.

```bash
python organizer.py list-course <course_number>
```

- **Example**:
  ```bash
  python organizer.py list-course 1
  ```

- **Output**:
  ```
  Section_01 (Lectures: 5/5):
    - Lecture_01_Introduction.mp4
    - Lecture_02_Variables.mp4

  Section_02 (Lectures: 2/5):
    - Lecture_01_Loops.mp4
    - Lecture_02_Conditionals.mp4
  ```

---

### **7. Calculate Total Video Duration**
Calculate the total duration of videos in the source directory.

```bash
python organizer.py calculate-total-length
```

- **Example Output**:
  ```
  Calculating Duration: 100%|██████████| 5/5 [00:05<00:00,  1.00video/s]
  Total video length: 50 minutes and 0 seconds.
  ```

---

## **Requirements**

The required dependencies are listed in `requirements.txt`. Install them with:
```bash
pip install -r requirements.txt
```

**Contents of `requirements.txt`:**
```
click==8.1.3
tqdm==4.67.0
```

---

## **Command Sequence for Testing**

Here’s the sequence of commands to test the functionality of the script:

1. **Generate Test Videos**:
   ```bash
   python organizer.py create-test-videos 5 --duration 10
   ```

2. **List Videos in Source Directory**:
   ```bash
   python organizer.py list-source-videos
   ```

3. **Rename a Video**:
   ```bash
   python organizer.py rename-video-command "Test_Video_01.mp4" "Introduction_to_Python.mp4"
   ```

4. **Create a New Course**:
   ```bash
   python organizer.py create-course 1
   ```

5. **Move Videos into the Course**:
   ```bash
   python organizer.py move-named-videos 1
   ```

6. **List the Course Contents**:
   ```bash
   python organizer.py list-course 1
   ```

7. **Calculate Total Video Duration**:
   ```bash
   python organizer.py calculate-total-length
   ```

---

## **Example Workflow**

Here’s how you can use the script step-by-step:

1. Generate 10 test videos in the source directory:
   ```bash
   python organizer.py create-test-videos 10 --duration 15
   ```

2. Check the source directory for the generated videos:
   ```bash
   python organizer.py list-source-videos
   ```

3. Rename one of the videos:
   ```bash
   python organizer.py rename-video-command "Test_Video_01.mp4" "Introduction_to_Python.mp4"
   ```

4. Create a new course:
   ```bash
   python organizer.py create-course 2
   ```

5. Move videos to the new course:
   ```bash
   python organizer.py move-named-videos 2
   ```

6. Check the course contents:
   ```bash
   python organizer.py list-course 2
   ```

---

## **License**

This tool is provided under the MIT License.

--- 

Let me know if you need further changes or additional details! 😊