from typing import Dict


def save_molviewspec(molviewspec: Dict, output_path: str):
    """Save MolViewSpec data to a JSON file"""
    import json

    with open(output_path, 'w') as f:
        json.dump(molviewspec, f, indent=2)