import numpy as np

from typing import Callable

from .helpers import (
    save_file_digests,
    add_noise,
    remove_noise,
    change_first_symbol_based_on_random_vector,
    reverse_change_first_symbol_based_on_random_vector,
    randomize_d_mod,
)
from .core.mutations.finite_field_mult_based import F8_MULT_BASED
from .core.base import BaseEncodeDecodeAlgorithm
from .precompute_multiplication import load_gf256

# NOTE: this is public key implementation of ecode_decode


def encode_bites_f8_mult_based_publickey(
    bites: np.ndarray,
    d_mod: int,
    encode_key: int,
    noise_ratio: float = 0.00,
):
    d_mod_range = randomize_d_mod(d_mod, encode_key)  # PRIVATE, never shared
    mul_lut = load_gf256()

    bites_mod = bites
    if noise_ratio > 0.0:
        bites_mod = add_noise(bites_mod, 256, encode_key, noise_ratio)

    algorithm = F8_MULT_BASED(bites_mod, d_mod_range)
    encoded = algorithm.encode()

    public_key = get_public_key(d_mod_range, mul_lut)  # SHARED public key
    return encoded, public_key


def decode_bites_f8_mult_based_publickey(
    bites: np.ndarray,
    public_key: np.ndarray,
    noise_ratio: float = 0.00,
):
    algorithm = F8_MULT_BASED(bites, public_key)
    decoded_bites = algorithm.decode(precomputed_inverses=public_key)

    if noise_ratio > 0.0:
        decoded_bites = remove_noise(decoded_bites, noise_ratio)

    return decoded_bites


def get_public_key(d_mod_range: np.ndarray, mul_lut: np.ndarray) -> np.ndarray:
    """
    Derive the public decode key from the private encode sequence.
    Each element is the GF(2^8) multiplicative inverse of the
    corresponding private a-value used during encoding.
    """
    public_key = np.zeros_like(d_mod_range, dtype=np.uint8)
    for i in range(len(d_mod_range)):
        a_raw = d_mod_range[i]
        a = np.uint8(1) if a_raw == 0 else np.uint8(a_raw)
        public_key[i] = np.where(mul_lut[a] == 1)[0][0]
    return public_key


if __name__ == "__main__":
    image_name = "img.jpg"
    # "C:\Users\Timofii\code\python\cryptall_2\tests\test_results\encoded\img_encoded.jpg"
    file_path = f"test_files/{image_name}"
    save_file_path = f"test_files/222_visual_encoded_{image_name}"
    save_file_digests(file_path, save_file_path)
