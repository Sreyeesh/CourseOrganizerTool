import os
import subprocess
import click
import shutil

# Define paths
SOURCE_DIR = r"C:\Users\sgari\Videos\Videos"
TARGET_DIR = r"C:\Users\sgari\Documents\UdemyCourses"
PREFIX = "TOUCAN_COURSE_"

# Helper function: Get folder size
def get_folder_size(folder_path):
    """Calculate the total size of a folder."""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

# Helper function: Get video duration using ffmpeg
def get_video_duration(video_path):
    """Get the duration of a video using ffprobe."""
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", video_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return float(result.stdout.strip())
    except Exception:
        return 0

@click.group()
def cli():
    """CLI Tool for managing videos and courses."""
    pass

@cli.command()
@click.argument("course_name")
@click.option("--source_dir", default=SOURCE_DIR, help="Directory containing the videos to rename.")
def qa_watch_and_rename(course_name, source_dir):
    """
    Quickly preview videos in the source directory, then rename them interactively.
    :param course_name: Name of the course.
    :param source_dir: Directory containing the videos.
    """
    try:
        # Detect video files
        video_files = sorted(
            [f for f in os.listdir(source_dir) if f.endswith(('.mp4', '.mkv', '.avi'))]
        )
        if not video_files:
            click.echo("No video files found in the source directory.")
            return

        click.echo(f"Total videos detected: {len(video_files)}\n")
        click.echo("You will quickly preview each video and rename it interactively.\n")

        for video_file in video_files:
            # Display the current file name
            click.echo(f"Current file: {video_file}")
            old_path = os.path.join(source_dir, video_file)

            # Open the video file in the default player
            click.echo("Opening video for quick preview...")
            subprocess.run(["start", old_path], shell=True, check=False)

            # Ask the user for a new name
            new_name = click.prompt("Enter the new name (without extension)", type=str)
            if not new_name.strip():
                click.echo("Skipping renaming for this file.\n")
                continue

            # Generate the new file name
            new_path = os.path.join(source_dir, f"{course_name}_{new_name.strip().replace(' ', '_')}.mp4")

            # Rename the file
            os.rename(old_path, new_path)
            click.echo(f"Renamed: {video_file} -> {os.path.basename(new_path)}\n")

        click.echo("Quick QA and renaming completed.")
    except Exception as e:
        click.echo(f"Error during QA and renaming: {e}")

@cli.command()
def list_courses():
    """List all existing TOUCAN course folders in the target directory."""
    try:
        existing_courses = [
            d for d in os.listdir(TARGET_DIR)
            if os.path.isdir(os.path.join(TARGET_DIR, d)) and d.startswith(PREFIX)
        ]
        if not existing_courses:
            click.echo("No TOUCAN course folders found in the target directory.")
            return

        click.echo("Existing TOUCAN course folders:")
        for course in sorted(existing_courses):
            course_path = os.path.join(TARGET_DIR, course)
            size_mb = get_folder_size(course_path) / (1024 * 1024)  # Convert size to MB
            click.echo(f"  - {course} ({size_mb:.2f} MB)")
    except Exception as e:
        click.echo(f"Error listing courses: {e}")

@cli.command()
@click.argument("course_number", type=int)
def show_course_details(course_number):
    """Show detailed information about a specific course."""
    try:
        course_folder = os.path.join(TARGET_DIR, f"{PREFIX}{course_number:03}")
        if not os.path.exists(course_folder):
            click.echo(f"Course folder does not exist: {course_folder}")
            return

        click.echo(f"Details for {PREFIX}{course_number:03}:\n")
        total_videos = 0
        total_duration = 0

        for section in sorted(os.listdir(course_folder)):
            section_path = os.path.join(course_folder, section)
            if os.path.isdir(section_path):
                click.echo(f"  {section}:")
                section_videos = [
                    f for f in os.listdir(section_path) if f.endswith(('.mp4', '.mkv', '.avi'))
                ]
                total_videos += len(section_videos)

                for video in section_videos:
                    video_path = os.path.join(section_path, video)
                    size_mb = os.path.getsize(video_path) / (1024 * 1024)  # Size in MB
                    duration = get_video_duration(video_path)
                    total_duration += duration

                    click.echo(f"    - {video}")
                    click.echo(f"      Size: {size_mb:.2f} MB, Duration: {duration / 60:.2f} minutes")

        total_duration_minutes = total_duration / 60
        click.echo("\nSummary:")
        click.echo(f"  Total Videos: {total_videos}")
        click.echo(f"  Total Duration: {total_duration_minutes:.2f} minutes")
    except Exception as e:
        click.echo(f"Error showing course details: {e}")

@cli.command()
@click.argument("course_number", type=int)
@click.option("--lectures_per_section", default=5, help="Number of lectures per section.")
def move_videos_to_course(course_number, lectures_per_section):
    """
    Move videos from SOURCE_DIR to a specific course folder and organize them into sections.
    :param course_number: Course number to move videos into.
    :param lectures_per_section: Maximum number of lectures per section.
    """
    try:
        # Define the course folder path
        course_folder = os.path.join(TARGET_DIR, f"{PREFIX}{course_number:03}")
        if not os.path.exists(course_folder):
            click.echo(f"Course folder does not exist: {course_folder}")
            return

        # Detect video files in the source directory
        video_files = [
            f for f in os.listdir(SOURCE_DIR) if f.endswith(('.mp4', '.mkv', '.avi'))
        ]
        if not video_files:
            click.echo("No videos found in the source directory.")
            return

        click.echo(f"Moving {len(video_files)} videos to {course_folder}...")

        # Initialize counters for sections and lectures
        section_number = 1
        lecture_number = 1

        # Create the first section folder if it doesn't exist
        section_folder = os.path.join(course_folder, f"Section_{section_number:02}")
        os.makedirs(section_folder, exist_ok=True)

        # Move and organize videos
        for video in video_files:
            old_path = os.path.join(SOURCE_DIR, video)
            new_name = f"Lecture_{lecture_number:02}_{video}"
            new_path = os.path.join(section_folder, new_name)

            shutil.move(old_path, new_path)
            click.echo(f"Moved: {video} -> {new_path}")

            lecture_number += 1
            if lecture_number > lectures_per_section:
                # Create a new section folder when the lecture limit is reached
                section_number += 1
                lecture_number = 1
                section_folder = os.path.join(course_folder, f"Section_{section_number:02}")
                os.makedirs(section_folder, exist_ok=True)

        click.echo("All videos have been moved and organized into sections.")
    except Exception as e:
        click.echo(f"Error moving videos: {e}")

@cli.command()
def calculate_total_duration():
    """Calculate the total duration of all videos in the source directory."""
    try:
        video_files = [
            os.path.join(SOURCE_DIR, f) for f in os.listdir(SOURCE_DIR)
            if f.endswith(('.mp4', '.mkv', '.avi'))
        ]
        if not video_files:
            click.echo("No videos found in the source directory.")
            return

        total_duration = 0
        for video in video_files:
            total_duration += get_video_duration(video)

        total_duration_minutes = total_duration / 60
        click.echo(f"Total video duration in source directory: {total_duration_minutes:.2f} minutes")
    except Exception as e:
        click.echo(f"Error calculating total duration: {e}")

@cli.command()
def list_source_videos():
    """List all videos in the source directory with their sizes and durations."""
    try:
        video_files = [
            f for f in os.listdir(SOURCE_DIR) if f.endswith(('.mp4', '.mkv', '.avi'))
        ]
        if not video_files:
            click.echo("No videos found in the source directory.")
            return

        click.echo("Videos in source directory:")
        for video in video_files:
            video_path = os.path.join(SOURCE_DIR, video)
            size_mb = os.path.getsize(video_path) / (1024 * 1024)  # Size in MB
            duration = get_video_duration(video_path)
            click.echo(f"  - {video}")
            click.echo(f"    Size: {size_mb:.2f} MB, Duration: {duration / 60:.2f} minutes")
    except Exception as e:
        click.echo(f"Error listing source videos: {e}")

if __name__ == "__main__":
    cli()
