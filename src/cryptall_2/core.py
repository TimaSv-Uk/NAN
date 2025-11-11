import numpy as np
from numba import njit

import os

# NOTE:
# np.uint8 used inted of  modulo operation only works with  mod 256

# NOTE:
# val = (x * y) & mod  # instead of % 256,
# only works if your modulus is a power of two


def encode_v5(
    chars: np.ndarray, char_encode_mod: int, d_mod_range: np.ndarray
) -> np.ndarray:
    """
    # (х_х1, х_2,..., х_п) і [у_1,у_2,..., у_п) коли
    #
    # х_2 - у_2 = у_1х_1
    # х_3 - у_3 = х_1у_2
    # х_4 - у_4 = у_1х_3
    # х_5 - у_5 = х_1у_4
    #
    # х_6 - у_6 = у_1х_5
    # х_7 - у_7 = х_1у_6
    #
    # y_1 = x_1+a1
    # y2 = x2 - ( (x_1+a1) * x1 )
    # y3 = x3 - (х_1 у_2)
    # Наш початковий вектор це X тобто всі Х відомі Треба знайти Y (сусідa) за
        формулою та використати його в якості X за модулем.
    """
    current_state = chars.astype(np.uint8).copy()
    next_state = np.empty_like(current_state)

    for a in d_mod_range:
        find_neighbors_v5(current_state, next_state, a, char_encode_mod)

        current_state, next_state = next_state, current_state

    return current_state


def decode_v5(
    chars: np.ndarray, char_encode_mod: int, d_mod_range: np.ndarray
) -> np.ndarray:
    """
    # (х_х1, х_2,..., х_п) і [у_1,у_2,..., у_п) коли
    #
    # х_2 - у_2 = у_1х_1
    # х_3 - у_3 = х_1у_2
    # х_4 - у_4 = у_1х_3
    # х_5 - у_5 = х_1у_4
    #
    # х_6 - у_6 = у_1х_5
    # х_7 - у_7 = х_1у_6
    #

    x_1 = y_1-a1
    x2 = y2 + ( (x_1+a1) * x1 )
    x3 = y3 + (х_1 у_2)
    x4 = y4 + (y_1 x_3)
    # Наш початковий вектор це X тобто всі Х відомі Треба знайти Y (сусідa) за
      формулою та використати його в якості X за модулем.
    """

    current_state = chars.astype(np.uint8).copy()
    next_state = np.empty_like(current_state)
    # Replace reversed(range(d_mod)) with a backward range for @jit

    for i in range(len(d_mod_range) - 1, -1, -1):
        a = d_mod_range[i]
        reverse_find_neighbors_v5(current_state, next_state, a, char_encode_mod)
        current_state, next_state = next_state, current_state  # Swap

    return current_state


def encode_v5_with_table(chars: np.ndarray, char_encode_mod: int, d_mod: int):
    BASE_DIR = os.path.dirname(__file__)
    mul_table_path = os.path.join(
        BASE_DIR, "multiplication_table", f"mul_mod_{char_encode_mod}.npy"
    )
    mul_table = np.load(mul_table_path)
    mul_table = mul_table.astype(np.uint16)  # optional for speed & memory

    current_state = chars.copy()
    next_state = np.empty_like(current_state)
    for a in range(d_mod):
        find_neighbors_v5_with_table(
            current_state, next_state, a, char_encode_mod, mul_table
        )
        current_state, next_state = next_state, current_state
    return current_state


@njit
def find_neighbors_v5_with_table(
    point_in: np.ndarray, point_out: np.ndarray, a: int, mod: int, mul_table
) -> None:
    """
    Calculates the next state and writes it into the pre-allocated
    point_out array.
    This version uses the precomputed multiplication table.

    point_in: The input array (X vector)
    point_out: The output array (Y vector)
    """
    n = len(point_in)

    # Calculate the first element (y1) and write it to the output array
    point_out[0] = (point_in[0] + a) % mod

    # Store x1 and y1 for reuse in the loop
    x0 = point_in[0]
    y0 = point_out[0]

    for i in range(1, n):
        if i % 2 == 0:
            # Even math index: y_i = x_i - (y1 * x_{i-1})
            # Use the multiplication table for y1 * x_{i-1}
            mult_result = mul_table[y0, point_in[i - 1]]
            point_out[i] = point_in[i] - mult_result
            # point_out[i] = temp % mod
            # point_out[i] = temp & mod
        else:
            # Odd math index: y_i = x_i - (x1 * y_{i-1})
            # Use the multiplication table for x1 * y_{i-1}
            mult_result = mul_table[x0, point_out[i - 1]]
            point_out[i] = point_in[i] - mult_result
            # point_out[i] = temp % mod
            # point_out[i] = temp & mod


@njit
def find_neighbors_v5(
    point_in: np.ndarray, point_out: np.ndarray, a: int, mod: int
) -> None:
    """
    point_in = (x1, x2, x3, ...)
    get Y node from X

    # index 1: y1 = x1 + a
    # even math index: y_i = x_i - (y1 * x_{i-1})
    # odd math index: y_i = x_i - (x1 * y_{i-1})

    """
    n = len(point_in)
    point_out[0] = (point_in[0] + a) % mod
    x0 = point_in[0]

    # NOTE:
    # val = (x) & mod  # instead of % 258, only works if your modulus is a power of two
    # automaticli aply mod 256 is use uint8
    for i in range(1, n):
        if i % 2 == 0:
            point_out[i] = np.uint8(point_in[i] - point_out[0] * point_in[i - 1])
            # temp = (point_in[i] - point_out[0] * point_in[i - 1])
            # point_out[i] = temp % mod
            # point_out[i] = temp & mod
        else:
            point_out[i] = np.uint8(point_in[i] - x0 * point_out[i - 1])
            # temp = (point_in[i] - x0 * point_out[i - 1])
            # point_out[i] = temp % mod
            # point_out[i] = temp & mod
    return None


@njit
def reverse_find_neighbors_v5(
    point_in: np.ndarray, point_out: np.ndarray, a: int, mod: int
) -> None:
    """
    point_in = [y1, y2, y3, ...]
    get X node from Y

    # index 1: x1 = y1 - a
    # even math index: x_i = y_i + y1 * x_{i-1}
    # odd math index: x_i = y_i + x1 * y_{i-1}

    """
    n = len(point_in)
    # point_out[0] = point_in[0] - a
    point_out[0] = (point_in[0] - a) % mod
    x0 = point_out[0]  # x1 is from the new array
    y0 = point_in[0]  # y1 is from the input array

    # NOTE:
    # np.uint8 used inted of  modulo operation only works with  mod 256
    # val = (x) & mod  # instead of % 258, only works if your modulus is a power of two
    # automaticli aply mod 256 is use uint8

    for i in range(1, n):
        if i % 2 == 0:
            point_out[i] = np.uint8(point_in[i] + y0 * point_out[i - 1])
            # point_out[i] = temp % mod
            # point_out[i] = temp & mod
        else:
            point_out[i] = np.uint8(point_in[i] + x0 * point_in[i - 1])
            # point_out[i] = temp % mod
            # point_out[i] = temp & mod
    return None


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


def randomize_d_mod(d_mod: int, seed: int) -> np.ndarray:
    if d_mod == 0:
        return np.arange(d_mod)

    np.random.seed(seed)
    index_to_randomize = np.random.randint(0, d_mod)
    random_val = np.random.randint(0, d_mod)
    range_d_mod = np.arange(d_mod, dtype=np.int64)

    while range_d_mod[index_to_randomize] == random_val:
        random_val = np.random.randint(0, d_mod)
    range_d_mod[index_to_randomize] = random_val

    return range_d_mod


@njit
def encode_assignment10(
    chars: np.ndarray, char_encode_mod: int, d_mod_range: np.ndarray, m: int
) -> np.ndarray:
    """
    improved version
    * from assighment5 graph algorithm

     (x1 x2 x3) [y1 = x1^m + a1, y2 = *,y3 = *]

     (y1 = x1 + a1 + a2, y2 = *,y3 = *)

     [y1 = x1^m + a1 + a2 + a3]

     (y1 = x1 + a1 + a2 + a3 + a4)
    """
    current_state = chars.astype(np.uint8).copy()
    next_state = np.empty_like(current_state)

    m = m % char_encode_mod

    for index in range(len(d_mod_range)):
        a = d_mod_range[index]
        # print(a)
        # print(d_mod_range[: index + 1])

        n = len(current_state)
        x0 = current_state[0]

        if index % 2 == 0:
            # y1 = x1^m
            next_state[0] = np.uint8((x0**m) + np.sum(d_mod_range[: index + 1]))
        else:
            # y1 = x1 + a1 + a2 + ... a_index
            next_state[0] = np.uint8(x0 + np.sum(d_mod_range[: index + 1]))

        for i in range(1, n):
            if i % 2 == 0:
                next_state[i] = np.uint8(
                    current_state[i] - next_state[0] * current_state[i - 1]
                )
            else:
                next_state[i] = np.uint8(current_state[i] - x0 * next_state[i - 1])

        current_state, next_state = next_state, current_state

    return current_state


@njit
def decode_assignment10(
    chars: np.ndarray, char_encode_mod: int, d_mod_range: np.ndarray, m: int
) -> np.ndarray:
    """
    improved version
    * from assighment5 graph algorithm

     (x1 x2 x3)

     [y1 = x1^m + a1, y2 = *,y3 = *]

     (x1 = y1 + a1 + a2, x2 = *,x3 = *)

     [y1 = x1^m + a1 + a2 + a3]

     (x1 = y1 + a1 + a2 + a3 + a4)
    """
    current_state = chars.astype(np.uint8).copy()
    next_state = np.empty_like(current_state)

    m = m % char_encode_mod

    current_state = chars.astype(np.uint8).copy()
    next_state = np.empty_like(current_state)

    for index in range(len(d_mod_range) - 1, -1, -1):
        a = d_mod_range[index]
        n = len(current_state)
        y0 = current_state[0]

        if index % 2 == 0:
            # TODO: need to fix decode
            # Reverse of: y0 = (x0**m + SUM) % mod
            next_state[0] = np.uint8(
                ((y0 ** (1 / m)) - np.sum(d_mod_range[: index + 1]))
            )
        else:
            # y1 = x1 + a1 + a2 + ... a_index
            next_state[0] = np.uint8(y0 - np.sum(d_mod_range[: index + 1]))

        x0 = next_state[0]

        for i in range(1, n):
            if i % 2 == 0:
                next_state[i] = np.uint8(current_state[i] + y0 * next_state[i - 1])
            else:
                next_state[i] = np.uint8(current_state[i] + x0 * current_state[i - 1])

        current_state, next_state = next_state, current_state

    return current_state
