import os
import shutil
import yaml
import click
from pathlib import Path
from moviepy.editor import VideoFileClip

def load_config():
    """Load paths and other configurations from config.yaml."""
    with open("config.yaml", "r") as file:
        return yaml.safe_load(file)

def load_course_outline():
    """Load the course outline from course_outline.yaml."""
    with open("course_outline.yaml", "r") as file:
        return yaml.safe_load(file)

def get_video_metadata(file_path):
    """Extract metadata such as duration and resolution from a video file."""
    with VideoFileClip(str(file_path)) as clip:  # Convert Path object to string
        duration = clip.duration  # Duration in seconds
        resolution = clip.size    # Resolution as [width, height]
    return {"duration": duration, "resolution": resolution}

def create_course_structure(course_path, sections):
    """Create folders for each section with titles from course_outline.yaml."""
    course_path.mkdir(parents=True, exist_ok=True)
    for section_title, lectures in sections.items():
        section_path = course_path / section_title
        section_path.mkdir(exist_ok=True)
        print(f"Created section folder: {section_path}")

def organize_videos(obs_video_path, course_path, course_outline):
    """Organize videos by moving and renaming them directly into the course structure."""
    video_files = sorted(
        [f for f in os.listdir(obs_video_path) if f.endswith(".mp4")],
        key=lambda f: os.path.getmtime(os.path.join(obs_video_path, f))
    )
    
    video_index = 0
    not_enough_videos = False
    
    for section_title, lectures in course_outline.items():
        section_folder = course_path / section_title
        section_folder.mkdir(parents=True, exist_ok=True)

        for lecture_title in lectures:
            if video_index < len(video_files):
                old_video_path = os.path.join(obs_video_path, video_files[video_index])
                metadata = get_video_metadata(old_video_path)
                print(f"Metadata for '{video_files[video_index]}': Duration = {metadata['duration']}s, "
                      f"Resolution = {metadata['resolution'][0]}x{metadata['resolution'][1]}")
                
                new_video_filename = f"{lecture_title}.mp4"
                new_video_path = section_folder / new_video_filename
                shutil.move(old_video_path, new_video_path)
                print(f"Moved '{video_files[video_index]}' to '{new_video_path}'")
                
                video_index += 1
            else:
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

def extract_metadata_from_organized_videos(course_path):
    """Extract metadata from videos in the organized course structure."""
    metadata_report = {}
    
    for section_folder in course_path.iterdir():
        if section_folder.is_dir():
            section_metadata = {}
            
            for video_file in section_folder.glob("*.mp4"):
                metadata = get_video_metadata(video_file)
                section_metadata[video_file.name] = metadata
                
                print(f"Metadata for '{video_file.name}' in '{section_folder.name}': "
                      f"Duration = {metadata['duration']}s, Resolution = {metadata['resolution'][0]}x{metadata['resolution'][1]}")
            
            metadata_report[section_folder.name] = section_metadata

    # Save the metadata report to a JSON file (optional)
    with open(course_path / "metadata_report.json", "w") as f:
        yaml.dump(metadata_report, f, default_flow_style=False)
    print("Metadata extraction complete. Report saved as 'metadata_report.json'.")

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

@cli.command(help="Extract metadata from videos in the organized course structure.")
def extract_metadata_cmd():
    """Extracts and prints metadata for each video in the organized course structure."""
    config = load_config()
    base_course_path = Path(config["base_course_path"])
    course_outline = load_course_outline()
    
    course_acronym = course_outline.get("course_acronym", "Default_Course")
    course_path = base_course_path / course_acronym
    
    extract_metadata_from_organized_videos(course_path)

if __name__ == "__main__":
    cli()
