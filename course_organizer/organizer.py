import os
import click
import shutil
import subprocess

# Define paths
SOURCE_DIR = r"C:\Users\sgari\Videos\Videos"
TARGET_DIR = r"C:\Users\sgari\Documents\UdemyCourses"

@click.group()
def cli():
    """CLI Tool for managing videos and courses."""
    pass

@cli.command()
def list_source_videos():
    """
    List all videos in the source directory with their sizes.
    """
    try:
        video_files = sorted(
            [f for f in os.listdir(SOURCE_DIR) if f.endswith(('.mp4', '.mkv', '.avi'))]
        )
        if not video_files:
            click.echo("No video files found in the source directory.")
            return

        click.echo("Videos in source directory:")
        for video in video_files:
            video_path = os.path.join(SOURCE_DIR, video)
            size_mb = os.path.getsize(video_path) / (1024 * 1024)
            click.echo(f"  - {video} ({size_mb:.2f} MB)")
    except Exception as e:
        click.echo(f"Error listing source videos: {e}")

@cli.command()
def quick_rename():
    """
    Quickly preview videos in SOURCE_DIR and rename them interactively.
    """
    video_files = sorted(
        [f for f in os.listdir(SOURCE_DIR) if f.endswith(('.mp4', '.mkv', '.avi'))]
    )
    if not video_files:
        click.echo("No video files found in the source directory.")
        return

    for video in video_files:
        old_path = os.path.join(SOURCE_DIR, video)
        click.echo(f"Current file: {video}")

        # Preview the video
        click.echo("Opening video for quick preview...")
        subprocess.run(["start", old_path], shell=True, check=False)

        # Prompt for a new name
        new_name = click.prompt("Enter the new name (e.g., Section01_Lecture01_Intro)", type=str).strip()
        if not new_name:
            click.echo("No name entered. Skipping this video.")
            continue

        # Rename the video
        new_path = os.path.join(SOURCE_DIR, f"{new_name}.mp4")
        os.rename(old_path, new_path)
        click.echo(f"Renamed: {video} -> {os.path.basename(new_path)}\n")

    click.echo("All videos have been renamed.")

@cli.command()
@click.argument("course_name")
@click.option("--sections", default=7, help="Number of sections to create.")
def create_course(course_name, sections):
    """
    Create a new course folder with specified sections.
    """
    try:
        course_folder = os.path.join(TARGET_DIR, course_name)
        os.makedirs(course_folder, exist_ok=True)

        for i in range(1, sections + 1):
            section_folder = os.path.join(course_folder, f"Section_{i:02}")
            os.makedirs(section_folder, exist_ok=True)

        click.echo(f"Course folder created: {course_folder} with {sections} sections.")
    except Exception as e:
        click.echo(f"Error creating course folder: {e}")

@cli.command()
@click.argument("course_name")
@click.option("--lectures_per_section", default=5, help="Max lectures per section.")
def move_videos_to_course(course_name, lectures_per_section):
    """
    Move renamed videos to the course folder, organizing them into sections.
    """
    try:
        video_files = sorted(
            [f for f in os.listdir(SOURCE_DIR) if f.endswith(('.mp4', '.mkv', '.avi'))]
        )
        if not video_files:
            click.echo("No videos found in the source directory.")
            return

        course_folder = os.path.join(TARGET_DIR, course_name)
        if not os.path.exists(course_folder):
            click.echo(f"Course folder does not exist: {course_folder}")
            return

        section_number = 1
        lecture_number = 1

        for video in video_files:
            # Create section folder if needed
            section_folder = os.path.join(course_folder, f"Section_{section_number:02}")
            os.makedirs(section_folder, exist_ok=True)

            # Move the video
            old_path = os.path.join(SOURCE_DIR, video)
            new_path = os.path.join(section_folder, video)
            shutil.move(old_path, new_path)
            click.echo(f"Moved: {video} -> {new_path}")

            # Increment counters
            lecture_number += 1
            if lecture_number > lectures_per_section:
                section_number += 1
                lecture_number = 1

        click.echo("Videos moved to course folder.")
    except Exception as e:
        click.echo(f"Error moving videos: {e}")

@cli.command()
@click.argument("course_name")
def list_course_details(course_name):
    """
    List details of a course folder, including sections and videos.
    """
    try:
        course_folder = os.path.join(TARGET_DIR, course_name)
        if not os.path.exists(course_folder):
            click.echo(f"Course folder does not exist: {course_folder}")
            return

        click.echo(f"Details for {course_name}:")
        for section in sorted(os.listdir(course_folder)):
            section_path = os.path.join(course_folder, section)
            if os.path.isdir(section_path):
                click.echo(f"  {section}:")
                for video in sorted(os.listdir(section_path)):
                    click.echo(f"    - {video}")
    except Exception as e:
        click.echo(f"Error listing course details: {e}")

@cli.command()
@click.argument("course_name")
def calculate_course_length(course_name):
    """
    Calculate the total video length for a specified course.
    """
    try:
        course_folder = os.path.join(TARGET_DIR, course_name)
        if not os.path.exists(course_folder):
            click.echo(f"Course folder does not exist: {course_folder}")
            return

        total_duration = 0
        video_count = 0

        for root, dirs, files in os.walk(course_folder):
            for file in files:
                if file.lower().endswith(('.mp4', '.mkv', '.avi')):
                    video_path = os.path.join(root, file)
                    try:
                        # Get video duration using ffprobe
                        result = subprocess.run(
                            [
                                "ffprobe", "-v", "error", "-show_entries",
                                "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", video_path
                            ],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            text=True,
                            check=True
                        )
                        duration = float(result.stdout.strip())
                        total_duration += duration
                        video_count += 1
                    except Exception as e:
                        click.echo(f"Error processing {file}: {e}")

        total_minutes = total_duration / 60
        click.echo(f"\nCourse: {course_name}")
        click.echo(f"  Total Videos: {video_count}")
        click.echo(f"  Total Duration: {total_minutes:.2f} minutes")
    except Exception as e:
        click.echo(f"Error calculating course length: {e}")

if __name__ == "__main__":
    cli()
