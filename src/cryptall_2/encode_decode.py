import numpy as np

import os
from typing import Callable

from .helpers import save_file_from_bites, load_file_to_bites, sudo_random_array
from .core import (
    encode_v5,
    decode_v5,
    change_first_symbol_based_on_full_vector,
    reverse_change_first_symbol_based_on_full_vector,
    change_first_symbol_based_on_random_vector,
    reverse_change_first_symbol_based_on_random_vector,
    randomize_d_mod,
)


def add_noise(
    bites: np.ndarray,
    char_ecncode_mod: int,
    seed: int,
    noise_ratio: float = 0.05,
) -> np.ndarray:
    """append vector of random bites to start of array; noise_ratio% lenght of original bites"""
    rand_arr_len = int(len(bites) * noise_ratio)
    bites_with_noise = np.append(
        sudo_random_array(rand_arr_len, char_ecncode_mod, seed, np.uint8), bites
    )
    return bites_with_noise


def remove_noise(
    bites: np.ndarray,
    char_ecncode_mod: int,
    seed: int,
    noise_ratio: float = 0.05,
):
    """remove vector of random bites from start of array; noise_ratio% lenght of original bites"""
    original_bites_len = int(len(bites) / (1 + noise_ratio))
    rand_arr_len = int(original_bites_len * noise_ratio)

    no_noise_bites = bites[rand_arr_len:]
    return no_noise_bites


def encode_bites(
    bites: np.ndarray,
    char_ecncode_mod: int,
    d_mod: int,
    seed: int,
    noise_ratio: float = 0.05,
) -> np.ndarray:
    bites = add_noise(bites, char_ecncode_mod, seed, noise_ratio)
    random_d_mod_range = np.arange(d_mod)
    file_bites = change_first_symbol_based_on_random_vector(bites, seed)
    encoded_bites = encode_v5(file_bites, char_ecncode_mod, random_d_mod_range)
    return encoded_bites


def decode_bites(
    bites: np.ndarray,
    char_ecncode_mod: int,
    d_mod: int,
    seed: int,
    noise_ratio: float = 0.05,
) -> np.ndarray:
    random_d_mod_range = np.arange(d_mod)
    decoded_bites = decode_v5(bites, char_ecncode_mod, random_d_mod_range)
    decoded_bites = reverse_change_first_symbol_based_on_random_vector(
        decoded_bites, seed
    )

    decoded_bites = remove_noise(decoded_bites, char_ecncode_mod, seed, noise_ratio)
    return decoded_bites


def encode_bites_rand(
    bites: np.ndarray, char_ecncode_mod: int, d_mod: int, seed: int
) -> np.ndarray:
    """Encode using random first-symbol modification."""
    d_range = randomize_d_mod(d_mod, seed)
    bites_mod = change_first_symbol_based_on_random_vector(bites, seed)
    return encode_v5(bites_mod, char_ecncode_mod, d_range)


def decode_bites_rand(
    bites: np.ndarray, char_ecncode_mod: int, d_mod: int, seed: int
) -> np.ndarray:
    """Decode using random first-symbol modification."""
    d_range = randomize_d_mod(d_mod, seed)
    bites_dec = decode_v5(bites, char_ecncode_mod, d_range)
    return reverse_change_first_symbol_based_on_random_vector(bites_dec, seed)


def encode_bites_full(
    bites: np.ndarray, char_ecncode_mod: int, d_mod: int, seed: int
) -> np.ndarray:
    """Encode using full-vector first-symbol modification."""
    d_range = randomize_d_mod(d_mod, seed)
    bites_mod = change_first_symbol_based_on_full_vector(bites)
    return encode_v5(bites_mod, char_ecncode_mod, d_range)


def decode_bites_full(
    bites: np.ndarray, char_ecncode_mod: int, d_mod: int, seed: int
) -> np.ndarray:
    """Decode using full-vector first-symbol modification."""
    d_range = randomize_d_mod(d_mod, seed)
    bites_dec = decode_v5(bites, char_ecncode_mod, d_range)
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
    return encode_v5(bites_mod, char_ecncode_mod, d_mod_range)


def decode_bites_select_func(
    bites: np.ndarray,
    char_ecncode_mod: int,
    seed: int,
    d_mod_range: np.ndarray,
    modify_vector_func: Callable[[np.ndarray], np.ndarray],
) -> np.ndarray:
    """Decode using full-vector/first-symbol modification."""
    bites_dec = encode_v5(bites, char_ecncode_mod, d_mod_range)
    return modify_vector_func(bites_dec)


def encode_file(
    file_path: str,
    save_encoded_file_path: str,
    seed: int = 42,
):
    char_ecncode_mod = 256
    d_mod = 128

    file_bites = load_file_to_bites(file_path)

    encoded_bites = encode_bites(file_bites, char_ecncode_mod, d_mod, seed)

    save_file_from_bites(save_encoded_file_path, encoded_bites)


def decode_file(
    encoded_file_path: str,
    save_decoded_file_path: str,
    seed: int = 42,
):
    char_ecncode_mod = 256
    d_mod = 128
    file_bites = load_file_to_bites(encoded_file_path)

    decoded_bites = decode_bites(file_bites, char_ecncode_mod, d_mod, seed)

    save_file_from_bites(save_decoded_file_path, decoded_bites)


def save_file_digests(
    digest_size: int,
    input_file_path: str,
    save_digests_dir_path: str,
):
    file_bites = load_file_to_bites(input_file_path)
    digests = np.array_split(file_bites, digest_size)
    for i, digest in enumerate(digests):
        os.makedirs(save_digests_dir_path, exist_ok=True)

        with open(f"{save_digests_dir_path}/{i}", "wb") as file:
            file.write(digest.tobytes())


if __name__ == "__main__":
    image_name = "img.jpg"
    # "C:\Users\Timofii\code\python\cryptall_2\tests\test_results\encoded\img_encoded.jpg"
    file_path = f"test_files/{image_name}"
    save_file_path = f"test_files/222_visual_encoded_{image_name}"
    save_file_digests(file_path, save_file_path)
