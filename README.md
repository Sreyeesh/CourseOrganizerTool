# Course Organizer Tool

The **Course Organizer Tool** is a command-line Python script that organizes course materials based on metadata like `provider`, `category`, `course_name`, `section`, and `lecture`. It renames and moves files into a structured folder hierarchy and includes a built-in course template to help structure your courses according to Udemy's standards.

---

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Flowchart of Actions](#flowchart-of-actions)
- [Examples](#examples)
- [Folder Structure](#folder-structure)

---

## Features
- Organize course files using standardized naming conventions.
- Built-in course template for Udemy-compliant course structure.
- Supports actions to set up folders, organize specific files, or organize all files in a directory.
- Customizable paths and categories via configuration file (`config.yaml`).

---

## Installation
1. Clone this repository or download the script.
2. Ensure you have Python 3 installed.

---

## Configuration
The tool uses a `config.yaml` file to define paths, categories, and the course template.

### Example `config.yaml`

```yaml
settings:
  root_folder: "C:\\Users\\sgari\\Documents\\UdemyCourses"
  categories:
    - "Python"
    - "DevOps"
    - "GameDevelopment"

paths:
  recording_directory: "C:\\Users\\sgari\\Videos\\Videos"
  default_filename: "lecture1.mp4"

course_template: |
  ### Udemy Course Template

  1. **Course Title**: e.g., "Mastering Python for Data Science"
  2. **Subtitle**: Brief, compelling description.
  3. **Course Description**: Detailed outline of course goals.
  4. **Learning Outcomes**: Specific skills students will gain.
  5. **Course Structure**: Organized by sections and lectures.
  6. **Video Lectures**: High-quality, engaging, with visuals.
  7. **Quizzes & Assignments**: For reinforcing concepts.
  8. **Supplementary Resources**: PDFs, code files, and readings.
  9. **Course Image**: 750 x 422 pixels, JPEG/PNG.
  10. **Promotional Video**: 1-2 minute intro video.
  11. **Final Project**: A hands-on project for portfolio.

  For full details, refer to the course documentation.
