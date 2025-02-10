# kids_calendar/settings.py
import yaml
from pathlib import Path

def load_settings():
    config_path = Path(__file__).parent / '../config.yaml'
    with open(config_path) as f:
        return yaml.safe_load(f)

settings = load_settings()
