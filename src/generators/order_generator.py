from pathlib import Path
from typing import Any
from src.config.config_loader import load_config
from src.generators.file_utils import get_initial_output_file, get_starting_order_number

import random

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

CONFIG_PATH = PROJECT_ROOT / "config" / "orders.yml"


def load_customers(config: dict[str, Any]) -> pd.DataFrame:
    """Load customers dataset."""

    path = PROJECT_ROOT / config["input"]["customers"]

    return pd.read_csv(path)


def load_products(config: dict[str, Any]) -> pd.DataFrame:
    """Load products dataset."""

    path = PROJECT_ROOT / config["input"]["products"]

    return pd.read_csv(path)


def generate_order(
    customers: pd.DataFrame,
    products: pd.DataFrame,
) -> dict[str, Any]:
    """
    Generate a single order.
    """

    customer = customers.sample(1).iloc[0]
    product = products.sample(1).iloc[0]

    quantity = random.randint(1, 5)

    discount = random.choice([0.00, 0.10, 0.20])

    revenue = round(
        quantity * product["unit_price"] * (1 - discount),
        2,
    )
    registration_date = pd.to_datetime(customer["registration_date"])

    days_after_registration = random.randint(0, 730)

    order_date = (registration_date + pd.Timedelta(days=days_after_registration)).date()

    return {
        "customer_id": customer["customer_id"],
        "product_id": product["product_id"],
        "order_date": order_date,
        "quantity": quantity,
        "unit_price": product["unit_price"],
        "discount": discount,
        "revenue": revenue,
    }


def generate_orders(
    customers: pd.DataFrame,
    products: pd.DataFrame,
    number_of_orders: int,
    starting_order_number: int,
) -> list[dict[str, Any]]:
    """
    Generate multiple orders.
    """

    orders = []

    for i in range(number_of_orders):
        order = generate_order(customers, products)

        order["order_id"] = f"O{starting_order_number + i:06d}"

        orders.append(order)

    return orders


def save_orders(
    orders: list[dict[str, Any]],
    output_path: Path,
) -> None:
    """
    Save orders to a CSV file.
    """

    df = pd.DataFrame(orders)

    df = df[
        [
            "order_id",
            "customer_id",
            "product_id",
            "order_date",
            "quantity",
            "unit_price",
            "discount",
            "revenue",
        ]
    ]

    df.to_csv(output_path, index=False)

    print(f"\nDataset saved to:\n{output_path}")


def main() -> None:
    config = load_config(CONFIG_PATH)

    output_directory = PROJECT_ROOT / config["output_directory"]
    output_prefix = config["output_prefix"]

    output_directory.mkdir(parents=True, exist_ok=True)

    output_path = get_initial_output_file(
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
        config["initial_number_of_orders"],
        starting_order_number,
    )

    print(f"Generated {len(orders)} orders.")

    save_orders(
        orders,
        output_path,
    )


if __name__ == "__main__":
    main()
