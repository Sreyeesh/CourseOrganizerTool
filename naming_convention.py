# organizer/naming_convention.py
from datetime import datetime

def sanitize_name(name):
    """Sanitize names for filenames and folders."""
    return name.replace(" ", "_").lower()

def generate_filename(provider, category, course_name, module, purpose, extension):
    """Generate a standardized filename based on convention."""
    timestamp = datetime.now().strftime("%m_%d_%Y")
    return f"{provider}_{sanitize_name(category)}_{sanitize_name(course_name)}_{sanitize_name(module)}_{purpose}_{timestamp}{extension}"
