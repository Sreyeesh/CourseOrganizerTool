# organizer/config_handler.py
import yaml
import os

CONFIG_FILE = "config.yaml"

def load_config():
    """Load YAML configuration."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            return yaml.safe_load(file)
    return {"settings": {"root_folder": "UdemyCourses", "categories": []}}

def save_config(config):
    """Save YAML configuration."""
    with open(CONFIG_FILE, "w") as file:
        yaml.dump(config, file)
