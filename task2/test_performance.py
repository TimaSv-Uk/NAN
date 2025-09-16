import time
import numpy as np
from helpers import load_file_to_bites
from task2 import (
    encode_assignment5_with_table,
    encode_assignment5,
    decode_assignment5,
)


def main():
    char_ecncode_mod = 256
    d_mod = 128

    # NOTE:
    # uint8 can store values from 0 to 255. lower X in unit_X gets faster execution time
    # sizes = {
    #     "10 B": 10,
    #     "1 MB": 1_000_000,
    #     "5 MB": 5_659_400,
    #     "10 MB": 10_000_000,
    #     "100 MB": 100_000_000,
    #     "1 GB": 1_000_000_000,
    # }
    #
    # selected_size_label = "100 MB"
    # size_in_elements = sizes[selected_size_label]
    #
    # text = np.array(
    #     [i % char_ecncode_mod for i in range(size_in_elements)], dtype=np.uint8
    # )
    # print(f"Generated array of size: {selected_size_label} ({text.nbytes} bytes)\n")

    # vid_31mb.mp4
    # big_img.JPG
    # text = load_file_to_bites("test_files/vid_31mb.mp4")
    text = load_file_to_bites("test_files/csv_123mb.csv")

    print(f"Generated array of size: {text.shape} bytes\n")

    start_time = time.perf_counter()
    encoded = encode_assignment5_with_table(text, char_ecncode_mod, d_mod)
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    print(f"WITH TABLE Encoded_vector execution_time: {execution_time}")

    start_time = time.perf_counter()
    encoded = encode_assignment5(text, char_ecncode_mod, d_mod)
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    print(f"Encoded_vector execution_time: {execution_time}")
    # print(f"Encoded_vector: {encoded}")

    start_time = time.perf_counter()
    decoded_vector = decode_assignment5(encoded, char_ecncode_mod, d_mod)
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    print(f"Decoded_vector execution_time: {execution_time}\n")
    # print(f"Decoded_vector: {decoded_vector}")

    if np.array_equal(text, decoded_vector):
        print("decoded_vector == text")
    else:
        print("decoded_vector =! text")


if __name__ == "__main__":
    main()
