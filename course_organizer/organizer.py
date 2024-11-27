import os
import shutil
import click
from tqdm import tqdm
from datetime import datetime
import subprocess

# Default paths
SOURCE_DIR = r"C:\Users\sgari\Videos\Videos"
TARGET_DIR = r"C:\Users\sgari\Documents\UdemyCourses"
COURSE_PREFIX = "TOUCAN_COURSE_"

@click.group()
def cli():
    """CLI Tool for organizing and managing videos."""
    pass

def get_next_course_number():
    """
    Determine the next available course number based on existing folders.
    """
    existing_courses = [
        d for d in os.listdir(TARGET_DIR) if d.startswith(COURSE_PREFIX)
    ]
    course_numbers = [
        int(d.replace(COURSE_PREFIX, "")) for d in existing_courses if d.replace(COURSE_PREFIX, "").isdigit()
    ]
    return max(course_numbers, default=0) + 1

def validate_and_sort_videos(source_dir):
    """
    Validate and sort videos by modification time.
    Returns a sorted list of video file paths.
    """
    video_files = [
        f for f in os.listdir(source_dir) if f.endswith(('.mp4', '.mkv', '.avi'))
    ]
    if not video_files:
        raise ValueError("No video files found in the source directory.")

    # Sort by modification time
    video_files.sort(key=lambda x: os.path.getmtime(os.path.join(source_dir, x)))
    return video_files

@cli.command()
@click.argument("course_name")
@click.option("--source_dir", default=SOURCE_DIR, help="Directory containing the videos to rename.")
@click.option("--preview", is_flag=True, help="Preview the renaming and moving process.")
def organize_videos(course_name, source_dir, preview):
    """
    Organize videos into the next available course folder with section subfolders.
    """
    try:
        # Validate and sort video files
        video_files = validate_and_sort_videos(source_dir)
        total_videos = len(video_files)
        required_videos = 7 * 5  # 7 sections x 5 videos each

        if total_videos != required_videos:
            click.echo(f"Error: Expected exactly {required_videos} videos, but found {total_videos}.")
            return

        # Determine the next course folder
        course_number = get_next_course_number()
        course_folder = f"{COURSE_PREFIX}{course_number:03}"
        course_path = os.path.join(TARGET_DIR, course_folder)
        os.makedirs(course_path, exist_ok=True)

        click.echo(f"Organizing {total_videos} videos into {course_folder}...")

        section_number = 1
        lecture_number = 1
        organize_preview = []

        for idx, video_file in enumerate(video_files):
            # Calculate section number (5 videos per section)
            if lecture_number > 5:
                section_number += 1
                lecture_number = 1

            # Generate the section folder
            section_folder = f"Section_{section_number:02}"
            section_path = os.path.join(course_path, section_folder)
            os.makedirs(section_path, exist_ok=True)

            # Generate the new name
            video_path = os.path.join(source_dir, video_file)
            timestamp = datetime.fromtimestamp(os.path.getmtime(video_path)).strftime("%Y%m%d_%H%M%S")
            new_name = f"{course_name}_S{section_number:02}_{timestamp}.mp4"
            organize_preview.append((video_file, new_name, section_path))

            lecture_number += 1

        if preview:
            click.echo("Preview of organization:")
            for original, new, section in organize_preview:
                click.echo(f"{original} -> {os.path.join(section, new)}")
            return

        # Perform renaming and moving
        with tqdm(total=len(organize_preview), desc="Organizing Videos", unit="file") as pbar:
            for original, new_name, section_path in organize_preview:
                old_path = os.path.join(source_dir, original)
                new_path = os.path.join(section_path, new_name)
                shutil.move(old_path, new_path)
                pbar.update(1)

        click.echo(f"Videos successfully organized into {course_folder}.")
    except Exception as e:
        click.echo(f"Error during organization: {e}")

@cli.command()
@click.option("--source_dir", default=SOURCE_DIR, help="Directory containing the videos to calculate duration.")
def calculate_total_length(source_dir):
    """
    Calculate the total length of all videos in the source directory using ffprobe.
    """
    video_files = [f for f in os.listdir(source_dir) if f.endswith(('.mp4', '.mkv', '.avi'))]
    if not video_files:
        click.echo(f"No video files found in {source_dir}.")
        return

    total_duration = 0
    click.echo(f"Calculating total duration for {len(video_files)} videos...")

    with tqdm(total=len(video_files), desc="Calculating Duration", unit="video") as pbar:
        for video in video_files:
            video_path = os.path.join(source_dir, video)
            duration = get_video_duration_ffprobe(video_path)
            total_duration += duration
            pbar.update(1)

    total_minutes = int(total_duration // 60)
    total_seconds = int(total_duration % 60)
    click.echo(f"Total video length: {total_minutes} minutes and {total_seconds} seconds.")

def get_video_duration_ffprobe(video_path):
    """
    Get the duration of a video using ffprobe from the ffmpeg package.
    """
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", video_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return float(result.stdout.strip())
    except Exception as e:
        click.echo(f"Error getting duration for {video_path}: {e}")
        return 0

if __name__ == "__main__":
    cli()
