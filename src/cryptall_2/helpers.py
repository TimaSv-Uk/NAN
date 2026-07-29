import numpy as np
from numba import njit

import os
# TODO: clean up, seperate d_mod_range,d_mod and change first_symbol groups of functions to seperate files


def sudo_random_array(length: int, d_mod: int, seed: int, dtype=int) -> np.ndarray:
    if length <= 0:
        return np.array([])
    rand_arr = np.empty([length], dtype=dtype)
    np.random.seed(seed)
    for i in range(length):
        random_val = np.random.randint(0, d_mod)
        rand_arr[i] = random_val

    return rand_arr


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


def bites_sameness_percentage(bites1: list[int], bites2: list[int]) -> float:
    if len(bites1) != len(bites2) or len(bites1) == 0:
        return 0.0
    same_symbols = sum(1 for a, b in zip(bites1, bites2) if a == b)
    return same_symbols / len(bites1)


def load_file_to_bites(file_name: str) -> np.ndarray:
    """Load file contents into a NumPy uint8 array."""
    if not os.path.exists(file_name):
        raise ValueError(f"File '{file_name}' does not exist.")
    with open(file_name, "rb") as file:
        bites = np.frombuffer(file.read(), dtype=np.uint8)
    return np.array(bites, dtype=np.uint8)


def load_file_to_bites_memmap(file_name: str) -> np.memmap:
    """Memory-map the file as a uint8 NumPy array (read-only)."""
    if not os.path.exists(file_name):
        raise ValueError(f"File '{file_name}' does not exist.")

    file_size = os.path.getsize(file_name)
    return np.memmap(file_name, dtype=np.uint8, mode="r", shape=(file_size,))


def read_large_file_generator(file_name: str, chunk_size: int) -> np.ndarray:
    if not os.path.exists(file_name):
        raise ValueError(f"File '{file_name}' does not exist.")
    with open(file_name, "r") as f:
        while True:
            bites = f.read(chunk_size)
            if not bites:
                break
            yield bites


def save_file_from_bites(file_name: str, data: np.ndarray) -> None:
    """Save a NumPy uint8 array back to a file."""
    try:
        with open(file_name, "wb") as file:
            file.write(data.tobytes())
        print(f"File saved successfully: {file_name}")
    except Exception as e:
        print(f"Error writing '{file_name}': {e}")


# NOTE:
# change_first_bite functions, if i put this in difirent file njit becomes realy slow and probsbly dont work
@njit
def change_first_symbol_based_on_random_vector(
    chars: np.ndarray, seed: int
) -> np.ndarray:
    new_chars = chars.astype(np.uint8).copy()
    if len(new_chars) < 2:
        return new_chars

    M = generate_M_from_seed(seed)

    new_chars[0] = chars[0] * M

    return new_chars


@njit
def reverse_change_first_symbol_based_on_random_vector(
    chars: np.ndarray, seed: int
) -> np.ndarray:
    new_chars = chars.astype(np.uint8).copy()
    if len(new_chars) < 2:
        return new_chars

    M = generate_M_from_seed(seed)

    M_inv = modInverse(M, 256)

    new_chars[0] = chars[0] * M_inv

    return new_chars


@njit
def change_first_symbol_based_on_full_vector(chars: np.ndarray) -> np.ndarray:
    """
    Calculates a new value for the first character in 'text' based on a weighted sum
    of all characters' modulo values, then applies 'char_encode_mod' to the result.

    Args:
        text (str): The input string.
        char_encode_mod (int): The modulus for character encoding and final calculation.

    Returns:
        list[int]: A list of integers with the modified first character's value
                   and the original modulo values for the rest.
    """
    new_chars = chars.astype(np.uint8).copy()
    # Make sure there are at least 2 elements
    if len(new_chars) < 2:
        return new_chars

    # NOTE:
    # Initialize M with a uint8 data type to ensure all subsequent
    # multiplications also wrap around at 256.

    M = np.uint8(1)

    for char_val in new_chars[1:]:
        M *= 2 * char_val + 1
        # M %= char_encode_mod

    # original_first_char_val = (new_chars[0] * M) % char_encode_mod
    original_first_char_val = new_chars[0] * M
    new_chars[0] = original_first_char_val

    return new_chars


@njit
def reverse_change_first_symbol_based_on_full_vector(chars: np.ndarray) -> np.ndarray:
    """
    Reverses the encoding performed by the `change_first_symbol_based_on_full_vector`
    function.

    Args:
        chars (np.ndarray): The input NumPy array of encoded integer values.

    Returns:
        np.ndarray: The decoded NumPy array.
    """
    new_chars = chars.astype(np.uint8).copy()

    if len(new_chars) < 2:
        return new_chars

    # Recalculate M from the array
    M = np.uint8(1)
    for char_val in new_chars[1:]:
        M *= 2 * char_val + 1

    # Get the modular inverse of M.
    # The inverse always exists because M is a product of odd numbers,
    # and 256 is a power of 2, so they are always coprime.
    M_inv = modInverse(M, 256)

    # Decode the first character
    original_first_char_val = new_chars[0] * M_inv
    new_chars[0] = original_first_char_val

    return new_chars


@njit
def generate_M_from_seed(seed: int) -> np.uint8:
    """Generate M value using seed without massive vector."""
    np.random.seed(seed)
    M = np.uint8(1)
    # small fixed number of iterations instead of file size
    for _ in range(32):
        val = np.random.randint(1, 256)
        M = (M * (2 * val + 1)) % 256  # Keep in uint8 range
    return M


# @njit
def generate_vector_of_bytes(size: int, seed: int | None = None) -> np.ndarray:
    """
    Generate vector or random bites:

    Args:
        size (int): Vector size (size x size).
        seed (int | None): Random seed for reproducibility.

    Returns:
        np.ndarray: The generated vector (dtype=uint8).
    """
    if seed is not None:
        np.random.seed(seed)

    vector = np.empty(size, np.uint8)

    for i in range(size):
        val = np.random.randint(1, 256)
        vector[i] = val
    return vector


@njit
def modInverse(a: int, m: int) -> int:
    """
    Calculates the modular multiplicative inverse of a modulo m
    using the Extended Euclidean Algorithm.
    This function is Numba-compatible.
    """
    m0, x0, x1 = m, 0, 1
    if m == 1:
        return 0
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += m0
    return x1


@njit
def randomize_d_mod(d_mod: int, seed: int) -> np.ndarray:
    range_d_mod = np.arange(d_mod, dtype=np.int64)

    if d_mod == 0:
        return range_d_mod

    index = seed % d_mod
    new_val = (seed * 1664525 + 1013904223) % d_mod  # LCG hash

    if new_val == index:
        new_val = (new_val + 1) % d_mod

    range_d_mod[index] = new_val
    return range_d_mod
