import time
import base64
import os
import numpy as np
from typing import Callable
from change_first_bite import (
    change_first_symbol_based_on_full_vector,
    reverse_change_first_symbol_based_on_full_vector,
    change_first_symbol_based_on_random_vector,
    reverse_change_first_symbol_based_on_random_vector,
)
from task2 import (
    encode_assignment5,
    decode_assignment5,
)


def encode_file(
    file_path="test_files/data2.txt",
    save_encoded_file_path="test_files/data2_encoded.txt",
):
    char_ecncode_mod = 256
    d_mod = 128
    seed = 42
    file_bites = load_file_to_bites(file_path)
    file_bites = change_first_symbol_based_on_random_vector(file_bites, seed)
    encoded_bites = encode_assignment5(file_bites, char_ecncode_mod, d_mod)
    save_file_from_bites(save_encoded_file_path, encoded_bites)


def decode_file(
    encoded_file_path="test_files/data2_encoded.txt",
    save_decoded_file_path="test_files/data2_decoded.txt",
):
    char_ecncode_mod = 256
    d_mod = 128
    seed = 42
    file_bites = load_file_to_bites(encoded_file_path)
    decoded_bites = decode_assignment5(file_bites, char_ecncode_mod, d_mod)
    decoded_bites = reverse_change_first_symbol_based_on_random_vector(
        decoded_bites, seed
    )

    save_file_from_bites(save_decoded_file_path, decoded_bites)


def get_encoded_text(
    text: str,
    char_ecncode_mod: int,
    d_mod: int,
) -> str:
    chars_uint8 = np.array(
        [ord(char) % char_ecncode_mod for char in text], dtype=np.uint8
    )

    encoded_with_first = change_first_symbol_based_on_full_vector(chars_uint8)

    encoded = encode_assignment5(encoded_with_first, char_ecncode_mod, d_mod)

    encoded_text = "".join(chr(int(x)) for x in encoded)
    return encoded_text


def get_decoded_text(
    encoded_text: str,
    char_ecncode_mod: int,
    d_mod: int,
) -> str:
    encoded_uint8 = np.array(
        [ord(char) % char_ecncode_mod for char in encoded_text], dtype=np.uint8
    )

    decoded = decode_assignment5(encoded_uint8, char_ecncode_mod, d_mod)

    reversed_first_symbol = reverse_change_first_symbol_based_on_full_vector(decoded)

    return "".join(chr(int(x)) for x in reversed_first_symbol)


def write_text_to_file(file_name, text):
    with open(file_name, "w") as f:
        f.write(text)


def text_from_int_to_ascii(point):
    decoded_text = [chr(int(element)) for element in point]
    return "".join(decoded_text)


def file_to_base64_txt(file_path, save_txt_path):
    with open(file_path, "rb") as file:
        encoded = base64.b64encode(file.read()).decode("utf-8")
    with open(save_txt_path, "w", encoding="utf-8") as txt_file:
        txt_file.write(encoded)


def base64_txt_to_file(text, output_file_path):
    decoded_data = base64.b64decode(text)
    with open(output_file_path, "wb") as output_file:
        output_file.write(decoded_data)


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


def load_file_to_bites(file_name: str) -> np.ndarray:
    """Load file contents into a NumPy uint8 array."""
    if not os.path.exists(file_name):
        print(f"Error: File '{file_name}' does not exist.")
        return np.array([], dtype=np.uint8)
    with open(file_name, "rb") as file:
        bites = np.frombuffer(file.read(), dtype=np.uint8)
    return np.array(bites, dtype=np.uint8)


def save_file_from_bites(file_name: str, data: np.ndarray) -> None:
    """Save a NumPy uint8 array back to a file."""
    try:
        with open(file_name, "wb") as file:
            file.write(data.tobytes())
        print(f"File saved successfully: {file_name}")
    except Exception as e:
        print(f"Error writing '{file_name}': {e}")


if __name__ == "__main__":
    file_path = "test_files/csv_123mb.csv"
    save_encoded_file_path = "test_files/csv_123mb_encoded.csv"
    save_decoded_file_path = "test_files/csv_123mb_decoded.csv"
    start_time = time.perf_counter()
    encode_file(file_path, save_encoded_file_path)
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    print(f"Encode file execution_time: {execution_time}")
    start_time = time.perf_counter()
    decode_file(save_encoded_file_path, save_decoded_file_path)
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    print(f"Decode file execution_time: {execution_time}")
