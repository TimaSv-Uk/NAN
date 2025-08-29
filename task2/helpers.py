import base64
import os
from typing import Callable


def get_encoded_text(
    text: str,
    char_ecncode_mod: int,
    d_mod: int,
    encode_function: Callable[[list[int], int, int], list[int]],
) -> str:
    # Import here to avoid circular imports
    from task2 import (
        get_change_first_symbol_based_on_full_vector,
    )

    chars_int = [ord(char) % char_ecncode_mod for char in text]
    encoded_with_first = get_change_first_symbol_based_on_full_vector(
        chars_int, char_ecncode_mod
    )
    encoded = encode_function(encoded_with_first, char_ecncode_mod, d_mod)
    encoded_text = text_from_int_to_ascii(encoded)
    return encoded_text


def get_decoded_text(
    encoded_text: str,
    char_ecncode_mod: int,
    d_mod: int,
    decode_function: Callable[[list[int], int, int], list[int]],
) -> str:
    # Import here to avoid circular imports
    from task2 import (
        reverse_change_first_symbol_based_on_full_vector,
    )

    encoded_int_from_text = [ord(char) % char_ecncode_mod for char in encoded_text]
    decoded = decode_function(encoded_int_from_text, char_ecncode_mod, d_mod)
    reversed_first_symbol = reverse_change_first_symbol_based_on_full_vector(
        decoded, char_ecncode_mod
    )
    return "".join([chr(i) for i in reversed_first_symbol])


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


if __name__ == "__main__":
    print(text_sameness_percentage("bon", "bob"))
