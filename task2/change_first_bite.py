import numpy as np
from numba import njit


# NOTE:
# np.uint8 used inted of  modulo operation only works with  mod 256


@njit
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
def change_first_symbol_based_on_random_vector(
    chars: np.ndarray, seed: int
) -> np.ndarray:
    new_chars = chars.astype(np.uint8).copy()
    # Make sure there are at least 2 elements
    if len(new_chars) < 2:
        return new_chars

    random_vector = generate_vector_of_bytes(len(chars), seed)

    M = np.uint8(1)

    for char_val in random_vector:
        M *= 2 * char_val + 1

    original_first_char_val = new_chars[0] * M
    new_chars[0] = original_first_char_val

    return new_chars


@njit
def reverse_change_first_symbol_based_on_random_vector(
    chars: np.ndarray, seed: int
) -> np.ndarray:
    new_chars = chars.astype(np.uint8).copy()
    if len(new_chars) < 2:
        return new_chars

    random_vector = generate_vector_of_bytes(len(chars), seed)

    M = np.uint8(1)
    for char_val in random_vector:
        M *= 2 * char_val + 1

    # Get the modular inverse of M.
    # The inverse always exists because M is a product of odd numbers,
    # and 256 is a power of 2, so they are always coprime.
    M_inv = modInverse(M, 256)

    original_first_char_val = new_chars[0] * M_inv
    new_chars[0] = original_first_char_val

    return new_chars


@njit
def change_first_symbol_based_on_full_vector(chars: np.ndarray) -> np.ndarray:
    """
    Calculates a new value for the first character in 'text' based on a weighted sum
    of all characters' modulo values, then applies 'char_ecncode_mod' to the result.

    Args:
        text (str): The input string.
        char_ecncode_mod (int): The modulus for character encoding and final calculation.

    Returns:
        list[int]: A list of integers with the modified first character's value
                   and the original modulo values for the rest.
    """
    new_chars = chars.copy().astype(np.uint8)
    # Make sure there are at least 2 elements
    if len(new_chars) < 2:
        return new_chars

    # NOTE:
    # Initialize M with a uint8 data type to ensure all subsequent
    # multiplications also wrap around at 256.

    M = np.uint8(1)

    for char_val in new_chars[1:]:
        M *= 2 * char_val + 1
        # M %= char_ecncode_mod

    # original_first_char_val = (new_chars[0] * M) % char_ecncode_mod
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
    new_chars = chars.copy().astype(np.uint8)
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


if __name__ == "__main__":
    mod = 256
    chars = np.array([10, 23, 23, 12, 123, 3213, 1])
    seed = 42
    new_first_bite_arr = change_first_symbol_based_on_random_vector(chars, seed)
    old_first_bite_arr = reverse_change_first_symbol_based_on_random_vector(
        new_first_bite_arr, seed
    )
    print(new_first_bite_arr, old_first_bite_arr)
