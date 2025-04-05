import random
import string
from pathlib import Path


def prepare(path: str):
    """
    Creates 5 random files in the specified directory path.

    Each file is created with a unique random name and are empty.
    This function is typically used for setting up a temporary test environment.

    Args:
        path (str): The directory path where the files should be created.
    """
    test_files = [
        Path(path) / ''.join(
            random.choices(string.ascii_letters + string.digits, k=40)
        )
        for _ in range(5)
    ]

    for file in test_files:
        file.touch()
