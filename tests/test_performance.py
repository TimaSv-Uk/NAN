import numpy as np

import time

from cryptall_2.helpers import load_file_to_bites
from cryptall_2.core import (
    encode_v5_with_table,
    encode_v5,
    decode_v5,
)


def main():
    char_ecncode_mod = 256
    d_mod = 128

    text = load_file_to_bites("test_files/vid_31mb.mp4")
    # text = load_file_to_bites("test_files/csv_123mb.csv")
    # text = load_file_to_bites("test_files/bob.txt")
    d_mod_range = np.arange(d_mod)

    print(f"Generated array of size: {text.shape} bytes\n")

    start_time = time.perf_counter()
    encoded = encode_v5_with_table(text, char_ecncode_mod, d_mod)
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    print(f"WITH TABLE Encoded_vector execution_time: {execution_time}")

    start_time = time.perf_counter()
    encoded = encode_v5(text, char_ecncode_mod, d_mod_range)
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    print(f"Encoded_vector execution_time: {execution_time}")
    print(f"Encoded_vector: {encoded}")

    start_time = time.perf_counter()
    decoded_vector = decode_v5(encoded, char_ecncode_mod, d_mod_range)
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    print(f"Decoded_vector execution_time: {execution_time}\n")
    print(f"Decoded_vector: {decoded_vector}")

    if np.array_equal(text, decoded_vector):
        print("decoded_vector == text")
    else:
        print("decoded_vector =! text")


if __name__ == "__main__":
    main()
