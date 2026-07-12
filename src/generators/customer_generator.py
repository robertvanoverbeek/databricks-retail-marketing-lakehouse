from pathlib import Path
from typing import Any

import yaml


# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Configuration file
CONFIG_PATH = PROJECT_ROOT / "config" / "customers.yml"


def load_config() -> dict[str, Any]:
    """
    Load the customer generator configuration.
    """

    with CONFIG_PATH.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def main() -> None:
    config = load_config()

    print("Customer Generator Configuration")
    print("--------------------------------")
    print(config)


if __name__ == "__main__":
    main()