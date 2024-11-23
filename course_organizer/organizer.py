import os
import shutil
import click
import subprocess
from tqdm import tqdm

# Define paths
SOURCE_DIR = r"C:\Users\sgari\Videos\Videos"
TARGET_DIR = r"C:\Users\sgari\Documents\UdemyCourses"
PREFIX = "TOUCAN_COURSE_"

# Ensure the target directory exists
os.makedirs(TARGET_DIR, exist_ok=True)

def get_next_course_number():
    """Determine the next course number."""
    existing_courses = [
        d for d in os.listdir(TARGET_DIR) if d.startswith(PREFIX)
    ]
    course_numbers = [
        int(d.replace(PREFIX, "")) for d in existing_courses if d.replace(PREFIX, "").isdigit()
    ]
    return max(course_numbers, default=0) + 1

def count_lectures(section_dir):
    """Count how many lectures are in a section."""
    return len([f for f in os.listdir(section_dir) if f.endswith(".mp4")])

def get_video_duration_ffmpeg(video_path):
    """Get the duration of a video using ffmpeg."""
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

def create_placeholder_video(output_path, title, duration=10, resolution="1920x1080", color="blue"):
    """Create a placeholder video using ffmpeg."""
    try:
        subprocess.run(
            [
                "ffmpeg",
                "-f", "lavfi",
                "-i", f"color=c={color}:s={resolution}:d={duration}",
                "-vf", f"drawtext=text='{title}':fontcolor=white:fontsize=48:x=(w-text_w)/2:y=(h-text_h)/2",
                "-y",  # Overwrite output file if it exists
                output_path
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True
        )
    except Exception as e:
        click.echo(f"Error creating placeholder video {output_path}: {e}")

@click.group()
def cli():
    """CLI Tool for organizing Udemy courses."""
    pass

@cli.command()
@click.argument("num_videos", type=int)
@click.option("--duration", default=10, help="Duration of each test video in seconds.")
def create_test_videos(num_videos, duration):
    """Create test videos in the source directory."""
    click.echo(f"Creating {num_videos} test videos in {SOURCE_DIR} with duration {duration}s each.")
    os.makedirs(SOURCE_DIR, exist_ok=True)

    with tqdm(total=num_videos, desc="Creating Test Videos", unit="video") as pbar:
        for i in range(1, num_videos + 1):
            video_title = f"Test_Video_{i:02}"
            video_path = os.path.join(SOURCE_DIR, f"{video_title}.mp4")
            create_placeholder_video(video_path, video_title, duration=duration, color="blue")
            pbar.update(1)

    click.echo(f"Created {num_videos} test videos in {SOURCE_DIR}.")

@cli.command()
@click.argument("course_number", type=int, required=False)
def create_course(course_number):
    """Create a new course directory with 7 sections."""
    if course_number is None:
        course_number = get_next_course_number()

    course_dir = os.path.join(TARGET_DIR, f"{PREFIX}{course_number:03}")
    if not os.path.exists(course_dir):
        os.makedirs(course_dir, exist_ok=True)
        for section_number in tqdm(range(1, 8), desc="Creating Sections", unit="section"):
            section_dir = os.path.join(course_dir, f"Section_{section_number:02}")
            os.makedirs(section_dir, exist_ok=True)
        click.echo(f"Created course directory: {course_dir} with 7 sections.")
    else:
        click.echo(f"Course directory already exists: {course_dir}")

@cli.command()
def list_source_videos():
    """List all videos in the source directory."""
    video_files = [f for f in os.listdir(SOURCE_DIR) if f.endswith(('.mp4', '.mkv', '.avi'))]
    if not video_files:
        click.echo("No video files found in the source directory.")
    else:
        click.echo("Videos in source directory:")
        for video in video_files:
            click.echo(f"  - {video}")

@cli.command()
@click.argument("old_name")
@click.argument("new_name")
def rename_video_command(old_name, new_name):
    """Rename a video in the source directory."""
    old_path = os.path.join(SOURCE_DIR, old_name)
    if not os.path.exists(old_path):
        click.echo(f"Video not found: {old_name}")
        return

    try:
        new_path = os.path.join(SOURCE_DIR, new_name)
        os.rename(old_path, new_path)
        click.echo(f"Renamed video: {old_name} -> {new_name}")
    except Exception as e:
        click.echo(f"Error renaming video: {e}")

@cli.command()
@click.argument("course_number", type=int)
def move_named_videos(course_number):
    """Move all named videos from the source directory to the course directory."""
    course_dir = os.path.join(TARGET_DIR, f"{PREFIX}{course_number:03}")
    if not os.path.exists(course_dir):
        click.echo(f"Course directory does not exist: {course_dir}")
        return

    video_files = [f for f in os.listdir(SOURCE_DIR) if f.endswith(".mp4")]
    if not video_files:
        click.echo(f"No videos found in {SOURCE_DIR}.")
        return

    total_videos = len(video_files)
    with tqdm(total=total_videos, desc="Moving Videos", unit="video") as pbar:
        for video in video_files:
            for section_number in range(1, 8):  # 7 sections
                section_dir = os.path.join(course_dir, f"Section_{section_number:02}")
                if not os.path.exists(section_dir):
                    os.makedirs(section_dir)

                lecture_count = count_lectures(section_dir)
                if lecture_count < 5:
                    source_path = os.path.join(SOURCE_DIR, video)
                    target_path = os.path.join(section_dir, video)
                    shutil.move(source_path, target_path)
                    click.echo(f"Moved: {video} -> {section_dir}")
                    pbar.update(1)
                    break
            else:
                click.echo("All sections are full. Cannot move more videos.")
                break

@cli.command()
def calculate_total_length():
    """Calculate the total length of all videos in the source directory."""
    video_files = [f for f in os.listdir(SOURCE_DIR) if f.endswith(('.mp4', '.mkv', '.avi'))]
    if not video_files:
        click.echo(f"No video files found in {SOURCE_DIR}.")
        return

    total_duration = 0
    with tqdm(total=len(video_files), desc="Calculating Duration", unit="video") as pbar:
        for video in video_files:
            video_path = os.path.join(SOURCE_DIR, video)
            total_duration += get_video_duration_ffmpeg(video_path)
            pbar.update(1)

    total_minutes = total_duration // 60
    total_seconds = total_duration % 60
    click.echo(f"Total video length: {int(total_minutes)} minutes and {int(total_seconds)} seconds.")

@cli.command()
@click.argument("course_number", type=int)
def list_course(course_number):
    """List all sections and lectures in a course."""
    course_dir = os.path.join(TARGET_DIR, f"{PREFIX}{course_number:03}")
    if not os.path.exists(course_dir):
        click.echo(f"Course directory does not exist: {course_dir}")
        return

    for section in os.listdir(course_dir):
        section_path = os.path.join(course_dir, section)
        if os.path.isdir(section_path):
            lecture_count = count_lectures(section_path)
            click.echo(f"\n{section} (Lectures: {lecture_count}/5):")
            lectures = os.listdir(section_path)
            for lecture in sorted(lectures):
                click.echo(f"  - {lecture}")

if __name__ == "__main__":
    cli()
