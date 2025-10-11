import numpy as np

import os


def get_unique_filename(base_name, suffix, extension):
    i = 1
    while True:
        filename = f"{base_name}_{suffix}_{i}.{extension}"
        if not os.path.exists(filename):
            return filename
        i += 1


def text_sameness_percentage(text1: str, text2: str) -> float:
    if len(text1) != len(text2) or len(text1) == 0:
        return 0.0
    same_symbols = sum(1 for a, b in zip(text1, text2) if a == b)
    return same_symbols / len(text1)


def bites_sameness_percentage(bites1: [int], bites2: [int]) -> float:
    if len(bites1) != len(bites2) or len(bites1) == 0:
        return 0.0
    same_symbols = sum(1 for a, b in zip(bites1, bites2) if a == b)
    return same_symbols / len(bites1)


def load_file_to_bites(file_name: str) -> np.ndarray:
    """Load file contents into a NumPy uint8 array."""
    if not os.path.exists(file_name):
        raise ValueError(f"File '{file_name}' does not exist.")
    with open(file_name, "rb") as file:
        bites = np.frombuffer(file.read(), dtype=np.uint8)
    return np.array(bites, dtype=np.uint8)


def load_file_to_bites_memmap(file_name: str) -> np.memmap:
    """Memory-map the file as a uint8 NumPy array (read-only)."""
    if not os.path.exists(file_name):
        raise ValueError(f"File '{file_name}' does not exist.")

    file_size = os.path.getsize(file_name)
    return np.memmap(file_name, dtype=np.uint8, mode="r", shape=(file_size,))


def read_large_file_generator(file_name: str, chunk_size: int) -> np.ndarray:
    if not os.path.exists(file_name):
        raise ValueError(f"File '{file_name}' does not exist.")
    with open(file_name, "r") as f:
        while True:
            bites = f.read(chunk_size)
            if not bites:
                break
            yield bites


def save_file_from_bites(file_name: str, data: np.ndarray) -> None:
    """Save a NumPy uint8 array back to a file."""
    try:
        with open(file_name, "wb") as file:
            file.write(data.tobytes())
        print(f"File saved successfully: {file_name}")
    except Exception as e:
        print(f"Error writing '{file_name}': {e}")
