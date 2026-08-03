from pathlib import Path
from src.generators.file_utils import get_starting_order_number


PROJECT_ROOT = Path(__file__).resolve().parents[2]


output_directory = PROJECT_ROOT / "data" / "generated"

print(get_starting_order_number(output_directory, "orders"))
