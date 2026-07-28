from pathlib import Path


def get_initial_output_file(
    output_directory: Path,
    output_prefix: str,
) -> Path:
    """
    Return the output path for the initial dataset.
    """

    return output_directory / f"{output_prefix}_001.csv"