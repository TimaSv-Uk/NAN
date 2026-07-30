import numpy as np

import os
from typing import Callable

from .helpers import (
    save_file_from_bites,
    load_file_to_bites,
    sudo_random_array,
    change_first_symbol_based_on_full_vector,
    reverse_change_first_symbol_based_on_full_vector,
    change_first_symbol_based_on_random_vector,
    reverse_change_first_symbol_based_on_random_vector,
    randomize_d_mod,
)
from .core.main_modulo import V5
from .core.sudo512_modulo import SUDO512_MOD
from .core.finite_field import F8
from .core.ring import RING
from .core.base import BaseEncodeDecodeAlgorithm


def _encode_pipeline(
    bites: np.ndarray,
    d_mod: int,
    seed: int,
    modifier_func: Callable[[np.ndarray], np.ndarray],
    algorithm_factory: Callable[[np.ndarray, np.ndarray], BaseEncodeDecodeAlgorithm],
    noise_ratio: float = 0.00,
    char_encode_mod: int = 256,
) -> np.ndarray:
    """Generic encoding pipeline to eliminate repeated boilerplate."""
    if noise_ratio > 0.0:
        bites = add_noise(bites, char_encode_mod, seed, noise_ratio)

    d_mod_range = randomize_d_mod(d_mod, seed)
    bites_mod = modifier_func(bites)
    algorithm = algorithm_factory(bites_mod, d_mod_range)
    return algorithm.encode()


def _decode_pipeline(
    bites: np.ndarray,
    d_mod: int,
    seed: int,
    algorithm_factory: Callable[[np.ndarray, np.ndarray], BaseEncodeDecodeAlgorithm],
    reverser_func: Callable[[np.ndarray], np.ndarray],
    noise_ratio: float = 0.00,
) -> np.ndarray:
    """Generic decoding pipeline to eliminate repeated boilerplate."""
    d_mod_range = randomize_d_mod(d_mod, seed)

    algorithm = algorithm_factory(bites, d_mod_range)
    decoded_bites = algorithm.decode()
    decoded_bites = reverser_func(decoded_bites)

    if noise_ratio > 0.0:
        decoded_bites = remove_noise(decoded_bites, noise_ratio)

    return decoded_bites


# --- IMPLEMENTATIONS ---


def encode_bites(
    bites: np.ndarray,
    char_encode_mod: int,
    d_mod: int,
    seed: int,
    noise_ratio: float = 0.00,
) -> np.ndarray:
    return _encode_pipeline(
        bites,
        d_mod,
        seed,
        modifier_func=lambda b: change_first_symbol_based_on_random_vector(b, seed),
        algorithm_factory=lambda b, d_range: V5(b, char_encode_mod, d_range),
        noise_ratio=noise_ratio,
        char_encode_mod=char_encode_mod,
    )


def decode_bites(
    bites: np.ndarray,
    char_encode_mod: int,
    d_mod: int,
    seed: int,
    noise_ratio: float = 0.00,
) -> np.ndarray:
    return _decode_pipeline(
        bites,
        d_mod,
        seed,
        algorithm_factory=lambda b, d_range: V5(b, char_encode_mod, d_range),
        reverser_func=lambda b: reverse_change_first_symbol_based_on_random_vector(
            b, seed
        ),
        noise_ratio=noise_ratio,
    )


def encode_bites_sudo512_mod(
    bites: np.ndarray,
    char_encode_mod: int,
    d_mod: int,
    seed: int,
    noise_ratio: float = 0.00,
) -> np.ndarray:

    return _encode_pipeline(
        bites,
        d_mod,
        seed,
        modifier_func=lambda b: change_first_symbol_based_on_random_vector(b, seed),
        algorithm_factory=lambda b, d_range: SUDO512_MOD(b, d_range),
        noise_ratio=noise_ratio,
        char_encode_mod=char_encode_mod,
    )


def decode_bites_sudo512_mod(
    bites: np.ndarray,
    char_encode_mod: int,
    d_mod: int,
    seed: int,
    noise_ratio: float = 0.00,
) -> np.ndarray:
    return _decode_pipeline(
        bites,
        d_mod,
        seed,
        algorithm_factory=lambda b, d_range: SUDO512_MOD(b, d_range),
        reverser_func=lambda b: reverse_change_first_symbol_based_on_random_vector(
            b, seed
        ),
        noise_ratio=noise_ratio,
    )


def encode_bites_f8(
    bites: np.ndarray,
    char_encode_mod: int,
    d_mod: int,
    seed: int,
    noise_ratio: float = 0.00,
) -> np.ndarray:

    return _encode_pipeline(
        bites,
        d_mod,
        seed,
        modifier_func=lambda b: change_first_symbol_based_on_random_vector(b, seed),
        algorithm_factory=lambda b, d_range: F8(b, d_range),
        noise_ratio=noise_ratio,
        char_encode_mod=char_encode_mod,
    )


def decode_bites_f8(
    bites: np.ndarray,
    char_encode_mod: int,
    d_mod: int,
    seed: int,
    noise_ratio: float = 0.00,
) -> np.ndarray:
    return _decode_pipeline(
        bites,
        d_mod,
        seed,
        algorithm_factory=lambda b, d_range: F8(b, d_range),
        reverser_func=lambda b: reverse_change_first_symbol_based_on_random_vector(
            b, seed
        ),
        noise_ratio=noise_ratio,
    )


def encode_bites_ring(
    bites: np.ndarray,
    char_encode_mod: int,
    d_mod: int,
    seed: int,
    noise_ratio: float = 0.00,
) -> np.ndarray:

    return _encode_pipeline(
        bites,
        d_mod,
        seed,
        modifier_func=lambda b: change_first_symbol_based_on_random_vector(b, seed),
        algorithm_factory=lambda b, d_range: RING(b, d_range),
        noise_ratio=noise_ratio,
        char_encode_mod=char_encode_mod,
    )


def decode_bites_ring(
    bites: np.ndarray,
    char_encode_mod: int,
    d_mod: int,
    seed: int,
    noise_ratio: float = 0.00,
) -> np.ndarray:
    return _decode_pipeline(
        bites,
        d_mod,
        seed,
        algorithm_factory=lambda b, d_range: RING(b, d_range),
        reverser_func=lambda b: reverse_change_first_symbol_based_on_random_vector(
            b, seed
        ),
        noise_ratio=noise_ratio,
    )


def encode_bites_rand(
    bites: np.ndarray, char_encode_mod: int, d_mod: int, seed: int
) -> np.ndarray:
    return _encode_pipeline(
        bites,
        d_mod,
        seed,
        modifier_func=lambda b: change_first_symbol_based_on_random_vector(b, seed),
        algorithm_factory=lambda b, d_range: V5(b, char_encode_mod, d_range),
    )


def decode_bites_rand(
    bites: np.ndarray, char_encode_mod: int, d_mod: int, seed: int
) -> np.ndarray:
    return _decode_pipeline(
        bites,
        d_mod,
        seed,
        algorithm_factory=lambda b, d_range: V5(b, char_encode_mod, d_range),
        reverser_func=lambda b: reverse_change_first_symbol_based_on_random_vector(
            b, seed
        ),
    )


def encode_bites_full(
    bites: np.ndarray, char_encode_mod: int, d_mod: int, seed: int
) -> np.ndarray:
    return _encode_pipeline(
        bites,
        d_mod,
        seed,
        modifier_func=lambda b: change_first_symbol_based_on_full_vector(b),
        algorithm_factory=lambda b, d_range: V5(b, char_encode_mod, d_range),
    )


def decode_bites_full(
    bites: np.ndarray, char_encode_mod: int, d_mod: int, seed: int
) -> np.ndarray:
    return _decode_pipeline(
        bites,
        d_mod,
        seed,
        algorithm_factory=lambda b, d_range: V5(b, char_encode_mod, d_range),
        reverser_func=lambda b: reverse_change_first_symbol_based_on_full_vector(b),
    )

# NOTE: old needs to be removed, and replaces in app to chose option of an algorithm
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

    number_of_digests = 4

    file_path = "tests/test_results/encoded/img_encoded.jpg"
    save_file_path = "tests/digests/img_encoded/"

    save_file_digests(number_of_digests, file_path, save_file_path)

    print(f"{number_of_digests} digests of {file_path}; Saved at {save_file_path}")


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
    noise_ratio: float = 0.00,
):
    """remove vector of random bites from start of array; noise_ratio% lenght of original bites"""
    original_bites_len = int(len(bites) / (1 + noise_ratio))
    rand_arr_len = int(original_bites_len * noise_ratio)

    no_noise_bites = bites[rand_arr_len:]
    return no_noise_bites


if __name__ == "__main__":
    image_name = "img.jpg"
    # "C:\Users\Timofii\code\python\cryptall_2\tests\test_results\encoded\img_encoded.jpg"
    file_path = f"test_files/{image_name}"
    save_file_path = f"test_files/222_visual_encoded_{image_name}"
    save_file_digests(file_path, save_file_path)
