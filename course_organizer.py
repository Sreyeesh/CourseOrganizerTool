import os
import yaml
import click
from pathlib import Path

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

def get_next_course_name():
    """Generate the next course name using the prefix and number in the config."""
    config = load_config()
    base_course_path = Path(config["base_course_path"])
    course_prefix = config["course_prefix"]
    starting_number = config["starting_course_number"]
    
    highest_number = starting_number - 1
    for folder in base_course_path.glob(f"{course_prefix}_*"):
        try:
            number = int(folder.name.split("_")[-1])
            highest_number = max(highest_number, number)
        except ValueError:
            continue
    next_course_number = highest_number + 1
    return f"{course_prefix}_{str(next_course_number).zfill(3)}"

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

def rename_videos_in_obs():
    """Rename videos sequentially in the OBS video path."""
    config = load_config()
    obs_video_path = Path(config["obs_video_path"])
    lectures_per_section = config["lectures_per_section"]
    
    # List and sort videos by modification date
    video_files = sorted(obs_video_path.glob("*.mp4"), key=lambda f: f.stat().st_mtime)
    if not video_files:
        print("No videos found in the OBS video path.")
        return
    
    print("\nFound the following videos:")
    for video in video_files:
        print(f" - {video.name}")
    
    # Rename each video sequentially as SectionXX_LectureYY
    section_count = 1
    lecture_count = 1
    for video_file in video_files:
        new_name = f"Section{str(section_count).zfill(2)}_Lecture{str(lecture_count).zfill(2)}.mp4"
        new_path = obs_video_path / new_name
        
        # Rename video
        video_file.rename(new_path)
        print(f"Renamed '{video_file.name}' to '{new_name}'")
        
        # Update counts
        lecture_count += 1
        if lecture_count > lectures_per_section:
            section_count += 1
            lecture_count = 1

def move_videos_to_course(course_path):
    """Move renamed videos to the correct section folders in the course directory."""
    config = load_config()
    obs_video_path = Path(config["obs_video_path"])
    
    # Iterate over each video in OBS path
    for video_file in obs_video_path.glob("Section*_Lecture*.mp4"):
        # Determine the section folder based on video name
        section_folder_name = video_file.stem.split("_")[0]  # e.g., "Section01"
        section_folder_path = course_path / section_folder_name
        section_folder_path.mkdir(parents=True, exist_ok=True)
        
        # Move the video to the correct section folder
        new_path = section_folder_path / video_file.name
        video_file.rename(new_path)
        print(f"Moved '{video_file.name}' to '{new_path}'")

@click.group()
def cli():
    """Course Organizer CLI: A tool to create course structure, rename videos, and move them."""
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

@cli.command(name="rename-videos")
def rename_videos_cmd():
    """Rename videos in OBS folder in sequential SectionXX_LectureYY format."""
    if not setup_check():
        return
    rename_videos_in_obs()
    print("\nVideo renaming completed.")

@cli.command(name="move-videos")
@click.argument("course_name")
def move_videos_cmd(course_name):
    """Move renamed videos from OBS folder to course section folders."""
    if not setup_check():
        return
    
    config = load_config()
    base_course_path = Path(config["base_course_path"])
    course_path = base_course_path / course_name
    if not course_path.exists():
        print(f"Error: Course folder '{course_name}' does not exist.")
        return
    
    move_videos_to_course(course_path)
    print("\nVideo moving completed.")

if __name__ == "__main__":
    cli()
