import os
import time

import numpy as np

from cryptall_2.helpers import (
    read_large_file_generator,
    load_file_to_bites,
    load_file_to_bites_memmap,
    save_file_from_bites,
)
from cryptall_2.core import (
    encode_v5_with_table,
    encode_assignment5,
    decode_assignment5,
)
from cryptall_2.encode_decode import encode_bites


def main():
    # === File paths ===
    # file_path = "tests/test_files/Audiobook_1gb.zip"
    file_path = "tests/test_files/csv_100mb.csv"
    # save_path = "tests/test_files/Encoded_Audiobook_1gb.zip"

    print("Mod: 128")

    start_time = time.perf_counter()
    bites_1 = load_file_to_bites_memmap(file_path)
    end_time = time.perf_counter()

    file_size_bytes = len(bites_1)
    file_size_kb = file_size_bytes / 1024
    file_size_mb = file_size_kb / 1024
    file_size_gb = file_size_mb / 1024

    print(
        f"File size: {file_size_bytes:,} bytes ({file_size_mb:.2f} MB / {
            file_size_gb:.3f} GB)"
    )
    print(f"Load time (memmap): {end_time - start_time:.4f} s")

    start_time = time.perf_counter()
    encoded = encode_bites(bites_1, 256, 128, 42)
    end_time = time.perf_counter()

    print(f"Encode time: {end_time - start_time:.4f} s")

    # === Optional: Save encoded output ===
    # start_time = time.perf_counter()
    # save_file_from_bites(save_path, encoded)
    # end_time = time.perf_counter()
    # print(f"Save time: {end_time - start_time:.4f} s")


if __name__ == "__main__":
    main()
