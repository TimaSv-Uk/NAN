import numpy as np

from typing import Callable

from .helpers import save_file_from_bites, load_file_to_bites
from .core import (
    encode_assignment5,
    decode_assignment5,
    change_first_symbol_based_on_full_vector,
    reverse_change_first_symbol_based_on_full_vector,
    change_first_symbol_based_on_random_vector,
    reverse_change_first_symbol_based_on_random_vector,
    randomize_d_mod,
)


def encode_bites(
    bites: np.ndarray, char_ecncode_mod: int, d_mod: int, seed: int
) -> np.ndarray:
    random_d_mod_range = np.arange(d_mod)
    file_bites = change_first_symbol_based_on_random_vector(bites, seed)
    encoded_bites = encode_assignment5(file_bites, char_ecncode_mod, random_d_mod_range)
    return encoded_bites


def decode_bites(
    bites: np.ndarray, char_ecncode_mod: int, d_mod: int, seed: int
) -> np.ndarray:
    random_d_mod_range = np.arange(d_mod)
    decoded_bites = decode_assignment5(bites, char_ecncode_mod, random_d_mod_range)
    decoded_bites = reverse_change_first_symbol_based_on_random_vector(
        decoded_bites, seed
    )
    return decoded_bites


def encode_bites_rand(
    bites: np.ndarray, char_ecncode_mod: int, d_mod: int, seed: int
) -> np.ndarray:
    """Encode using random first-symbol modification."""
    d_range = randomize_d_mod(d_mod, seed)
    bites_mod = change_first_symbol_based_on_random_vector(bites, seed)
    return encode_assignment5(bites_mod, char_ecncode_mod, d_range)


def decode_bites_rand(
    bites: np.ndarray, char_ecncode_mod: int, d_mod: int, seed: int
) -> np.ndarray:
    """Decode using random first-symbol modification."""
    d_range = randomize_d_mod(d_mod, seed)
    bites_dec = decode_assignment5(bites, char_ecncode_mod, d_range)
    return reverse_change_first_symbol_based_on_random_vector(bites_dec, seed)


def encode_bites_full(
    bites: np.ndarray, char_ecncode_mod: int, d_mod: int, seed: int
) -> np.ndarray:
    """Encode using full-vector first-symbol modification."""
    d_range = randomize_d_mod(d_mod, seed)
    bites_mod = change_first_symbol_based_on_full_vector(bites)
    return encode_assignment5(bites_mod, char_ecncode_mod, d_range)


def decode_bites_full(
    bites: np.ndarray, char_ecncode_mod: int, d_mod: int, seed: int
) -> np.ndarray:
    """Decode using full-vector first-symbol modification."""
    d_range = randomize_d_mod(d_mod, seed)
    bites_dec = decode_assignment5(bites, char_ecncode_mod, d_range)
    return reverse_change_first_symbol_based_on_full_vector(bites_dec)


def encode_bites_select_func(
    bites: np.ndarray,
    char_ecncode_mod: int,
    seed: int,
    d_mod_range: np.ndarray,
    modify_vector_func: Callable[[np.ndarray], np.ndarray],
) -> np.ndarray:
    """Encode using full-vector/first-symbol modification."""
    bites_mod = modify_vector_func(bites)
    return encode_assignment5(bites_mod, char_ecncode_mod, d_mod_range)


def decode_bites_select_func(
    bites: np.ndarray,
    char_ecncode_mod: int,
    seed: int,
    d_mod_range: np.ndarray,
    modify_vector_func: Callable[[np.ndarray], np.ndarray],
) -> np.ndarray:
    """Decode using full-vector/first-symbol modification."""
    bites_dec = encode_assignment5(bites, char_ecncode_mod, d_mod_range)
    return modify_vector_func(bites_dec)


def encode_file(
    file_path: str = "test_files/data2.txt",
    save_encoded_file_path: str = "test_files/data2_encoded.txt",
    seed: int = 42,
):
    char_ecncode_mod = 256
    d_mod = 128

    file_bites = load_file_to_bites(file_path)

    encoded_bites = encode_bites(file_bites, char_ecncode_mod, d_mod, seed)

    save_file_from_bites(save_encoded_file_path, encoded_bites)


def decode_file(
    encoded_file_path: str = "test_files/data2_encoded.txt",
    save_decoded_file_path: str = "test_files/data2_decoded.txt",
    seed: int = 42,
):
    char_ecncode_mod = 256
    d_mod = 128
    file_bites = load_file_to_bites(encoded_file_path)

    decoded_bites = decode_bites(file_bites, char_ecncode_mod, d_mod, seed)

    save_file_from_bites(save_decoded_file_path, decoded_bites)


if __name__ == "__main__":
    image_name = "img.jpg"

    file_path = f"test_files/{image_name}"
    save_file_path = f"test_files/222_visual_encoded_{image_name}"

    encode_file(file_path, save_file_path)
