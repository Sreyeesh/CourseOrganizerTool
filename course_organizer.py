import os
import shutil
import yaml
import click
from pathlib import Path

def load_config():
    """Load paths and other configurations from config.yaml."""
    with open("config.yaml", "r") as file:
        return yaml.safe_load(file)

def load_course_outline():
    """Load the course outline from course_outline.yaml."""
    with open("course_outline.yaml", "r") as file:
        return yaml.safe_load(file)

def create_course_structure(course_path, sections):
    """Create folders for each section with titles from course_outline.yaml."""
    course_path.mkdir(parents=True, exist_ok=True)
    for section_title, lectures in sections.items():
        section_path = course_path / section_title
        section_path.mkdir(exist_ok=True)
        print(f"Created section folder: {section_path}")

def organize_videos(obs_video_path, course_path, course_outline):
    """Organize videos by moving and renaming them directly into the course structure."""
    
    # Get a list of all video files in the OBS path, sorted by modification time
    video_files = sorted(
        [f for f in os.listdir(obs_video_path) if f.endswith(".mp4")],
        key=lambda f: os.path.getmtime(os.path.join(obs_video_path, f))
    )
    
    # Keep track of video index to map them sequentially
    video_index = 0
    not_enough_videos = False  # Flag to track if there were insufficient videos
    
    for section_title, lectures in course_outline.items():
        section_folder = course_path / section_title
        section_folder.mkdir(parents=True, exist_ok=True)

        for lecture_title in lectures:
            if video_index < len(video_files):
                # Use the next video file based on modification order
                old_video_path = os.path.join(obs_video_path, video_files[video_index])
                
                # Format the new video filename based on lecture title
                new_video_filename = f"{lecture_title}.mp4"
                new_video_path = section_folder / new_video_filename
                
                # Move and rename the video file
                shutil.move(old_video_path, new_video_path)
                print(f"Moved '{video_files[video_index]}' to '{new_video_path}'")
                
                # Increment to the next video file
                video_index += 1
            else:
                # If we run out of videos, set the flag
                not_enough_videos = True
                break

    if not_enough_videos:
        print("Warning: Not enough videos to match the course outline.")

def rename_videos(course_path, outline_file="course_outline.yaml"):
    """Rename videos within the course structure based on their location in the outline."""
    with open(outline_file, "r") as file:
        course_outline = yaml.safe_load(file)

    section_titles = course_outline["sections"]

    for section_title, lectures in section_titles.items():
        section_folder = course_path / section_title
        videos = sorted([f for f in os.listdir(section_folder) if f.endswith(".mp4")])
        
        for video, lecture_title in zip(videos, lectures):
            new_name = f"{lecture_title}.mp4"
            old_path = section_folder / video
            new_path = section_folder / new_name
            os.rename(old_path, new_path)
            print(f"Renamed {old_path} to {new_path}")

@click.group()
def cli():
    """Course Organizer CLI: A tool to create structure, organize, and rename videos."""
    pass

@cli.command(help="Create course folder structure based on the outline.")
def create_structure():
    """Creates the folder structure for the course."""
    config = load_config()
    course_outline = load_course_outline()
    base_course_path = Path(config["base_course_path"])
    course_acronym = course_outline.get("course_acronym", "Default_Course")
    course_path = base_course_path / course_acronym
    
    print(f"\nCreating structure for course at: {course_path}")
    create_course_structure(course_path, course_outline["sections"])

@cli.command(help="Organize recorded videos into the course folder structure.")
def organize_videos_cmd():
    """Moves and organizes videos based on the course outline."""
    config = load_config()
    course_outline = load_course_outline()
    obs_video_path = config["obs_video_path"]
    
    # Define the target course path directly in base_course_path/course_acronym
    base_course_path = Path(config["base_course_path"])
    course_acronym = course_outline.get("course_acronym", "Default_Course")
    course_path = base_course_path / course_acronym
    
    organize_videos(obs_video_path, course_path, course_outline["sections"])
    print("Video organization complete.")

@cli.command(help="Rename videos in the course structure based on the outline.")
def rename_videos_cmd():
    """Renames videos to follow the course outline convention."""
    config = load_config()
    base_course_path = Path(config["base_course_path"])
    course_outline = load_course_outline()
    
    course_acronym = course_outline.get("course_acronym", "Default_Course")
    course_path = base_course_path / course_acronym
    
    rename_videos(course_path)
    print("Video renaming complete.")

if __name__ == "__main__":
    cli()
