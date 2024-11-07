import os
import yaml
import click
from pathlib import Path
from moviepy.editor import VideoFileClip
import re

def load_config():
    """Load paths and other configurations from config.yaml."""
    with open("config.yaml", "r") as file:
        return yaml.safe_load(file)

def setup_check():
    """Check if configuration and necessary paths exist."""
    config = load_config()
    base_course_path = Path(config["base_course_path"])
    obs_video_path = Path(config["obs_video_path"])
    
    if not base_course_path.exists():
        print(f"Error: Base course path {base_course_path} does not exist.")
        return False
    if not obs_video_path.exists():
        print(f"Error: OBS video path {obs_video_path} does not exist.")
        return False
    print("Setup check completed. Configuration and paths are valid.")
    return True

def create_course_and_section_folders(course_name):
    """Creates the main course folder and section subfolders."""
    config = load_config()
    base_course_path = Path(config["base_course_path"])
    course_path = base_course_path / course_name
    
    course_path.mkdir(parents=True, exist_ok=True)
    print(f"Created main course folder: {course_path}")
    
    sections_per_course = config["sections_per_course"]
    for section_num in range(1, sections_per_course + 1):
        section_folder_name = f"Section{str(section_num).zfill(2)}"
        section_folder_path = course_path / section_folder_name
        section_folder_path.mkdir(exist_ok=True)
        print(f"Created section folder: {section_folder_path}")
    return course_path

def move_videos_to_course(course_name):
    """Move renamed videos to the appropriate section folders in the course directory."""
    config = load_config()
    obs_video_path = Path(config["obs_video_path"])
    base_course_path = Path(config["base_course_path"])
    course_path = base_course_path / course_name

    # Verify course folder exists
    if not course_path.exists():
        print(f"Error: Course folder '{course_path}' does not exist.")
        return

    # Locate and move each video to the appropriate section folder
    for video_file in obs_video_path.glob("Section*_Lecture*.mp4"):
        # Extract section number from the filename
        match = re.match(r"(Section\d{2})_Lecture\d{2}\.mp4", video_file.name)
        if match:
            section_folder_name = match.group(1)  # e.g., "Section01"
            section_folder_path = course_path / section_folder_name
            
            # Verify the section folder exists
            if section_folder_path.exists():
                # Move the video to the appropriate section folder
                new_path = section_folder_path / video_file.name
                video_file.rename(new_path)
                print(f"Moved '{video_file.name}' to '{new_path}'")
            else:
                print(f"Warning: Section folder '{section_folder_path}' does not exist. Skipping '{video_file.name}'.")

@click.group()
def cli():
    """Course Organizer CLI: A tool to create course structure, rename, and move videos."""
    pass

@cli.command(name="setup-check")
def setup_check_cmd():
    """Run setup check for paths and configuration."""
    setup_check()

@cli.command(name="create-course")
@click.argument("course_name")
def create_course_cmd(course_name):
    """Create course folder with section subfolders."""
    if not setup_check():
        return
    course_path = create_course_and_section_folders(course_name)
    print(f"\nCourse '{course_name}' created successfully with section folders.")

@cli.command(name="move-videos")
@click.argument("course_name")
def move_videos_cmd(course_name):
    """Move renamed videos from OBS folder to course section folders."""
    if not setup_check():
        return
    move_videos_to_course(course_name)
    print("\nVideo moving process completed.")

if __name__ == "__main__":
    cli()
