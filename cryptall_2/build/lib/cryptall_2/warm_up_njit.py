import numpy as np

from .helpers import load_file_to_bites
from .core import (
    encode_assignment5,
    encode_assignment5_with_table,
    decode_assignment5,
    change_first_symbol_based_on_random_vector,
    reverse_change_first_symbol_based_on_random_vector,
)


def warm_up(seed: int = 42):
    # Small dummy array
    dummy = np.array([1, 2, 3, 4], dtype=np.uint8)

    # Call all njit functions once to trigger compilation
    _ = change_first_symbol_based_on_random_vector(dummy, seed)
    _ = reverse_change_first_symbol_based_on_random_vector(dummy, seed)
    _ = encode_assignment5(dummy, 256, 2)
    _ = decode_assignment5(dummy, 256, 2)
    _ = encode_assignment5_with_table(dummy, 256, 2)


if __name__ == "__main__":
    # Warm-up all njit functions
    warm_up(seed=32312)

    # Now run your actual timing with large arrays
    text = load_file_to_bites("test_files/csv_123mb.csv")
    # text = load_file_to_bites("test_files/vid_31mb.mp4")

    import time

    start_time = time.perf_counter()
    encoded = encode_assignment5_with_table(text, 256, 128)
    end_time = time.perf_counter()
    print("Encoded with table:", end_time - start_time)

    start_time = time.perf_counter()
    encoded = encode_assignment5(text, 256, 128)
    end_time = time.perf_counter()
    print("Encoded:", end_time - start_time)

    start_time = time.perf_counter()
    decoded = decode_assignment5(encoded, 256, 128)
    end_time = time.perf_counter()
    print("Decoded:", end_time - start_time)
