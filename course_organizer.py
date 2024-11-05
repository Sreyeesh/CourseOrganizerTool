import os
import yaml
import click
import pdfplumber
import re
from pathlib import Path

def load_config():
    """Load paths and other configurations from config.yaml."""
    with open("config.yaml", "r") as file:
        return yaml.safe_load(file)

def create_main_course_folder(base_course_path, course_name):
    """Creates the main course folder with hidden .pdf and .metadata subfolders."""
    course_path = base_course_path / course_name
    course_path.mkdir(parents=True, exist_ok=True)
    
    # Create hidden folders for .pdf and .metadata
    pdf_folder = course_path / ".pdf"
    metadata_folder = course_path / ".metadata"
    pdf_folder.mkdir(exist_ok=True)
    metadata_folder.mkdir(exist_ok=True)
    
    print(f"Created main course folder: {course_path}")
    print(f"Created hidden .pdf and .metadata folders inside {course_path}")
    return course_path

def parse_pdf_outline(file_path):
    """Parse sections from the PDF file and ensure multiple sections are captured."""
    course_outline = {"sections": {}}

    with pdfplumber.open(file_path) as pdf:
        # Loop through all pages if necessary
        for page in pdf.pages:
            lines = page.extract_text().splitlines()

            # Assume the first line is the course title/acronym
            course_acronym = lines[0].strip().replace(" ", "_")
            print(f"Parsed course acronym: {course_acronym}")

            for line in lines[1:]:
                line = line.strip()
                
                # Detect section titles based on "Section" pattern
                section_match = re.match(r"^Section\s+\d+:\s+(.+)", line)
                if section_match:
                    section_title = section_match.group(1).strip()
                    course_outline["sections"][section_title] = []  # Add each section title with an empty list for lectures

    course_outline["course_acronym"] = course_acronym
    return course_outline

def simplify_title(title, max_words=5):
    """Simplify a title by using only the first few words, with a max limit for clarity."""
    words = title.split()[:max_words]
    return "_".join(words)

def create_section_folders(course_path, course_outline):
    """Create a folder for each section title found in the PDF."""
    sections = course_outline["sections"]
    
    for index, section_title in enumerate(sections.keys(), start=1):
        # Format folder name as "01_Simplified_Title"
        simplified_title = simplify_title(section_title)
        section_folder_name = f"{index:02d}_{simplified_title}"
        section_path = course_path / section_folder_name
        section_path.mkdir(exist_ok=True)
        print(f"Created section folder: {section_path}")

@click.group()
def cli():
    """Course Organizer CLI: A tool to create main folder, subfolder structure, organize, and update course outline."""
    pass

@cli.command(name="create-course-folder", help="Create the main course folder with hidden .pdf and .metadata folders.")
@click.argument("course_name")
def create_course_folder(course_name):
    """Creates the main course folder structure."""
    config = load_config()
    base_course_path = Path(config["base_course_path"])
    create_main_course_folder(base_course_path, course_name)

@cli.command(name="create-subfolders-from-pdf", help="Create section folders from the PDF outline.")
@click.argument("course_name")
def create_subfolders_from_pdf_cmd(course_name):
    """Creates section folders based on the PDF content in the .pdf folder of the main course folder."""
    config = load_config()
    base_course_path = Path(config["base_course_path"])
    course_path = base_course_path / course_name

    if not course_path.exists():
        print(f"Error: Main course folder '{course_path}' does not exist. Please create it first.")
        return

    pdf_folder = course_path / ".pdf"
    pdf_files = list(pdf_folder.glob("*.pdf"))

    if not pdf_files:
        print("Error: No PDF file found in the .pdf folder.")
        return

    pdf_path = pdf_files[0]
    course_outline = parse_pdf_outline(pdf_path)
    
    create_section_folders(course_path, course_outline)

if __name__ == "__main__":
    cli()
