from pathlib import Path
from typing import Any
import pandas as pd

import yaml
from faker import Faker


# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Configuration file
CONFIG_PATH = PROJECT_ROOT / "config" / "customers.yml"

fake = Faker()


def load_config() -> dict[str, Any]:
    """
    Load the customer generator configuration.
    """
    with CONFIG_PATH.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def generate_customer(config: dict[str, Any]) -> dict[str, Any]:
    """
    Generate a single customer.
    """
    return {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email(),
        "country": fake.random_element(config["countries"]),
        "registration_date": fake.date_between(
            start_date="-5y",
            end_date="today",
        ),
        "marketing_opt_in": fake.boolean(
            chance_of_getting_true=int(config["marketing_opt_in_rate"] * 100)
        ),
        "loyalty_tier": fake.random_element(config["loyalty_tiers"]),
    }


def generate_customers(
    config: dict[str, Any],
) -> list[dict[str, Any]]:
    """
    Generate multiple customer records.
    """

    customers = []

    for i in range(1, config["number_of_customers"]):
        customer = generate_customer(config)

        customer["customer_id"] = f"C{i:06d}"

        customers.append(customer)

    return customers

def save_customers(
    customers: list[dict[str, Any]],
    config: dict[str, Any],
) -> None:
    """
    Save customers to a CSV file.
    """

    output_path = PROJECT_ROOT / config["output_file"]

    output_path.parent.mkdir(parents=True, exist_ok=True)

    df = pd.DataFrame(customers)

    df.to_csv(output_path, index=False)

    print(f"\nDataset saved to:\n{output_path}")

def main() -> None:
    config = load_config()

    customers = generate_customers(config)

    print(f"Generated {len(customers)} customers\n")



  #  for customer in customers:
 #       print(customer)

    save_customers(customers, config)


if __name__ == "__main__":
    main()