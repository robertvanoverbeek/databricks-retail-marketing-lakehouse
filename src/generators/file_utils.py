from pathlib import Path

from traitlets import Int
import csv


def get_initial_output_file(
    output_directory: Path,
    output_prefix: str,
) -> Path:
    """
    Return the output path for the initial dataset.
    """

    return output_directory / f"{output_prefix}_001.csv"


def get_next_output_file(
    output_directory: Path,
    output_prefix: str,
) -> Path:
    """Return the output path for the next batch dataset."""

    batch_files = list(output_directory.glob(f"{output_prefix}_*.csv"))

    if not batch_files:
        return get_initial_output_file(
            output_directory,
            output_prefix,
        )

    batch_numbers = []

    for file in batch_files:
        batch_number = int(file.stem.split("_")[-1])
        batch_numbers.append(batch_number)

    highest_batch = max(batch_numbers)
    next_batch = highest_batch + 1
    next_output_file = output_directory / f"{output_prefix}_{next_batch:03d}.csv"
    return next_output_file


def get_starting_order_number(
    output_directory: Path,
    output_prefix: str,
) -> int:

    batch_files = list(output_directory.glob(f"{output_prefix}_*.csv"))

    if not batch_files:
        return 1

    batch_numbers = []

    for file in batch_files:
        batch_number = int(file.stem.split("_")[-1])
        batch_numbers.append(batch_number)

    highest_batch = max(batch_numbers)
    last_output_file = output_directory / f"{output_prefix}_{highest_batch:03d}.csv"
    return get_last_order_number(last_output_file) + 1


def get_last_order_number(last_output_file: Path) -> int:
    with last_output_file.open(
        "r",
        newline="",
        encoding="utf-8",
    ) as csvfile:
        reader = csv.reader(csvfile)

        next(reader)

        last_row = None

        for row in reader:
            last_row = row

    return int(last_row[0][1:])
