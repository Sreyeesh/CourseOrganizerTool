import yaml
import click
from pathlib import Path
import re
import logging
from moviepy.editor import VideoFileClip

# Initialize logging
logging.basicConfig(filename="course_organizer.log", level=logging.INFO, format="%(asctime)s - %(message)s")

def load_config():
    """Load paths and other configurations from config.yaml."""
    with open("config.yaml", "r") as file:
        return yaml.safe_load(file)

def calculate_total_video_duration(course_path):
    """Calculate the total duration of all videos in a course folder and save metadata."""
    total_duration = 0
    course_name = course_path.stem  # Course folder name

    # Loop through all video files in the course folder and subfolders
    for video_file in course_path.rglob("*.mp4"):
        with VideoFileClip(str(video_file)) as clip:
            total_duration += clip.duration
    
    # Convert total duration to hours, minutes, seconds format
    hours = int(total_duration // 3600)
    minutes = int((total_duration % 3600) // 60)
    seconds = int(total_duration % 60)
    
    total_duration_str = f"{hours}h {minutes}m {seconds}s"
    print(f"{course_name} - Total duration of videos: {total_duration_str}")

    # Save metadata to a file in the course folder
    metadata_file = course_path / f"{course_name}_metadata.txt"
    with open(metadata_file, "w") as file:
        file.write(f"Course Name: {course_name}\n")
        file.write(f"Total Length: {total_duration_str}\n")

    print(f"Metadata saved to: {metadata_file}")

@click.group()
def cli():
    """Course Organizer CLI: A tool to calculate video length and organize videos."""
    pass

@cli.command(name="calculate-total-video-length")
def calculate_total_video_length_cmd():
    """Calculate and display the total duration of all videos in each course folder and save metadata."""
    config = load_config()
    base_course_path = Path(config["base_course_path"])

    # Iterate through all TOUCAN_COURSE_### folders
    for course_folder in base_course_path.glob("TOUCAN_COURSE_*"):
        if course_folder.is_dir():
            calculate_total_video_duration(course_folder)

    print("\nTotal video duration calculation and metadata file creation completed.")

if __name__ == "__main__":
    cli()
