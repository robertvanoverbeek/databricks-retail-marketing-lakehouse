from pathlib import Path
from typing import Any
import random

import pandas as pd
import yaml
from faker import Faker


# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Configuration file
CONFIG_PATH = PROJECT_ROOT / "config" / "products.yml"

fake = Faker()


def load_config() -> dict[str, Any]:
    """
    Load the product generator configuration.
    """

    with CONFIG_PATH.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file)

def generate_product(config: dict[str, Any]) -> dict[str, Any]:
    category = random.choice(list(config["categories"].keys()))
    category_config = config["categories"][category]

    brand = random.choice(category_config["brands"])
    product_name = random.choice(category_config["product_names"])

    min_price = category_config["price_range"]["min"]
    max_price = category_config["price_range"]["max"]

    unit_price = round(random.uniform(min_price, max_price), 2)

    return {
        "category": category,
        "brand": brand,
        "product_name": product_name,
        "unit_price": unit_price,
    }

def generate_products(
    config: dict[str, Any],
) -> list[dict[str, Any]]:

    products = []

    for i in range(1, config["number_of_products"] + 1):
        product = generate_product(config)

        product["product_id"] = f"P{i:06d}"

        products.append(product)

    return products 


def save_products(
    products: list[dict[str, Any]],
    config: dict[str, Any],
) -> None:
    """
    Save products to a CSV file.
    """

    output_path = PROJECT_ROOT / config["output_file"]

    output_path.parent.mkdir(parents=True, exist_ok=True)

    df = pd.DataFrame(products)

    df.to_csv(output_path, index=False)

    print(f"\nDataset saved to:\n{output_path}")


def main() -> None:
    config = load_config()

    products = generate_products(config)

    print(f"Generated {len(products)} products.")

    save_products(products, config)


if __name__ == "__main__":
    main()