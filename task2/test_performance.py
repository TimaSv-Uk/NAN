import time
import numpy as np
from helpers import (
    get_decoded_text,
    get_encoded_text,
)
from task2 import (
    encode_assignment5_with_table,
    encode_assignment5,
    decode_assignment5,
)


def main():
    char_ecncode_mod = 258
    d_mod = 128
    # text = [i for i in range(258)]
    # text = np.array([i % char_ecncode_mod for i in range(10)], dtype=np.int64)
    # # text = "".join([f"{i}" for i in range(50000)])
    # text = [i % char_ecncode_mod for i in range(10)]
    # text = np.array([i % char_ecncode_mod for i in range(1000000)], dtype=np.int64)
    text = np.array([i % char_ecncode_mod for i in range(5659400)], dtype=np.int64)
    # text = np.arange(5659400, dtype=np.int32)
    # print(np.arange(10, dtype=np.int32))
    # 5659400

    start_time = time.perf_counter()
    encoded = encode_assignment5_with_table(text, char_ecncode_mod, d_mod)
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    print(f"WITH TABLE Encoded_vector execution_time: {execution_time}")

    # encoded_vector = get_encoded_text(text, char_ecncode_mod, d_mod, encode_assignment5)
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
    print(f"Decoded_vector execution_time: {execution_time}")
    # print(f"Decoded_vector: {decoded_vector}")


if __name__ == "__main__":
    main()
