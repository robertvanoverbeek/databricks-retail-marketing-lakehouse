from pathlib import Path
from typing import Any

import yaml


def load_config(config_path: Path) -> dict[str, Any]:
    """Load a YAML configuration file."""

    with config_path.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file)
