from pathlib import Path

from src.config.config_loader import load_config
from src.generators.file_utils import get_next_output_file
from src.generators.order_generator import (
    generate_orders,
    load_customers,
    load_products,
    save_orders,
    get_starting_order_number,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = PROJECT_ROOT / "config" / "orders.yml"


def main() -> None:
    config = load_config(CONFIG_PATH)

    output_directory = PROJECT_ROOT / config["output_directory"]
    output_prefix = config["output_prefix"]

    output_directory.mkdir(parents=True, exist_ok=True)

    output_path = get_next_output_file(
        output_directory,
        output_prefix,
    )

    starting_order_number = get_starting_order_number(
        output_directory,
        output_prefix,
    )

    customers = load_customers(config)
    products = load_products(config)

    orders = generate_orders(
        customers,
        products,
        config["batch_number_of_orders"],
        starting_order_number,
    )

    save_orders(
        orders,
        output_path,
    )

    print(f"Generated {len(orders)} orders.")
    print(f"Saved batch to: {output_path}")


if __name__ == "__main__":
    main()
