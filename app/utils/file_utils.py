# File handling utilities
import json
from typing import Optional, Dict, Any

def load_json(file_path: str) -> Optional[Dict[str, Any]]:
    """Load JSON file safely."""
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading JSON: {e}")
        return None

def save_json(data: Dict[str, Any], file_path: str) -> bool:
    """Save data to JSON file."""
    try:
        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving JSON: {e}")
        return False