from sympy import Matrix
import numpy as np
from numba import njit
from precompute_multiplication import read_precompute_multiplication


# NOTE:
# val = (x * y) & mod  # instead of % 256, only works if your modulus is a power of two
def multiply_mod(x: int, mod: int):
    # Check if mod is power of two
    if (mod & (mod - 1)) == 0:
        mask = mod - 1
        return (x) & mask
    else:
        return (x) % mod


def get_change_first_symbol_based_on_full_vector(
    chars: list[int], char_ecncode_mod: int
) -> list[int]:
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
    new_chars = list(chars)
    # Make sure there are at least 2 elements
    if len(new_chars) < 2:
        return new_chars

    M = 1
    for char_val in new_chars[1:]:
        M *= 2 * char_val + 1
        M %= char_ecncode_mod

    original_first_char_val = (new_chars[0] * M) % char_ecncode_mod
    new_chars[0] = original_first_char_val

    return new_chars


def reverse_change_first_symbol_based_on_full_vector(
    chars: list[int], char_ecncode_mod: int
) -> list[int]:
    """
    Why the inverse always exists
    For any integer xi, 2 * xi is even.
    So, 2 * xi + 1 is always odd.

    M = (2 * x2 + 1) * (2 * x3+1) ... (2 * xn+1)

    x1' => x1 * M
    x1 = x1' / M
    """
    new_chars = list(chars)
    # Make sure there are at least 2 elements
    if len(new_chars) < 2:
        return new_chars

    M = 1
    for char_val in new_chars[1:]:
        M *= 2 * char_val + 1
        M %= char_ecncode_mod

    try:
        M_inv = pow(M, -1, char_ecncode_mod)
    except ValueError:
        raise ValueError(f"M = {M} has no modular inverse modulo {char_ecncode_mod}")

    original_first_char_val = (new_chars[0] * M_inv) % char_ecncode_mod
    new_chars[0] = original_first_char_val

    return new_chars


def encode_assignment5_with_table(chars: np.ndarray, char_encode_mod: int, d_mod: int):
    # Load table once
    mul_table = np.load(f"multiplication_table/mul_mod_{char_encode_mod}.npy")
    mul_table = mul_table.astype(np.uint16)  # optional for speed & memory

    current_state = chars.copy()
    next_state = np.empty_like(current_state)
    for a in range(d_mod):
        find_neighbors_assignment5_with_table(
            current_state, next_state, a, char_encode_mod, mul_table
        )
        current_state, next_state = next_state, current_state
    return current_state


@njit
def find_neighbors_assignment5_with_table(
    point_in: np.ndarray, point_out: np.ndarray, a: int, mod: int, mul_table
) -> None:
    """
    Calculates the next state and writes it into the pre-allocated point_out array.
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
def encode_assignment5(
    chars: np.ndarray, char_ecncode_mod: int, d_mod: int
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
    # Наш початковий вектор це X тобто всі Х відомі Треба знайти Y (сусідa) за формулою та використати його в якості X за модулем.
    """

    current_state = chars.copy()
    next_state = np.empty_like(current_state)

    for a in range(d_mod):
        find_neighbors_assignment5(current_state, next_state, a, char_ecncode_mod)

        current_state, next_state = next_state, current_state

    return current_state


@njit
def decode_assignment5(
    chars: np.ndarray, char_ecncode_mod: int, d_mod: int
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
    # Наш початковий вектор це X тобто всі Х відомі Треба знайти Y (сусідa) за формулою та використати його в якості X за модулем.
    """

    current_state = chars.copy()
    next_state = np.empty_like(current_state)
    # Replace reversed(range(d_mod)) with a backward range for @jit
    for a in range(d_mod - 1, -1, -1):
        reverse_find_neighbors_assignment5(
            current_state, next_state, a, char_ecncode_mod
        )
        current_state, next_state = next_state, current_state  # Swap

    return current_state


@njit
def find_neighbors_assignment5(
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
    # point_out[0] = point_in[0] + a
    point_out[0] = (point_in[0] + a) % mod
    x0 = point_in[0]

    # NOTE:
    # val = (x) & mod  # instead of % 258, only works if your modulus is a power of two
    # automaticli aply mod 256 is use uint8
    for i in range(1, n):
        if i % 2 == 0:
            point_out[i] = point_in[i] - point_out[0] * point_in[i - 1]
            # point_out[i] = temp % mod
            # point_out[i] = temp & mod
        else:
            point_out[i] = point_in[i] - x0 * point_out[i - 1]
            # point_out[i] = temp % mod
            # point_out[i] = temp & mod
    return None


@njit
def reverse_find_neighbors_assignment5(
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
    # val = (x) & mod  # instead of % 258, only works if your modulus is a power of two
    # automaticli aply mod 256 is use uint8

    for i in range(1, n):
        if i % 2 == 0:
            point_out[i] = point_in[i] + y0 * point_out[i - 1]
            # point_out[i] = temp % mod
            # point_out[i] = temp & mod
        else:
            point_out[i] = point_in[i] + x0 * point_in[i - 1]
            # point_out[i] = temp % mod
            # point_out[i] = temp & mod
    return None


# TODO: assignment6


# def change_full_vector_with_matrix(
#     chars: list[int], char_ecncode_mod: int, matrix_seed
# ) -> list[int]:
#     """
#     Encodes a vector using a randomly generated invertible matrix (modular arithmetic).
#
#     Args:
#         chars (list[int]): Input vector of integers to encode.
#         char_ecncode_mod (int): The modulus for modular arithmetic (e.g. 258).
#         matrix_seed (int): Seed for the random generator to ensure reproducibility.
#
#     Returns:
#         list[int]: Encoded vector (same length as input).
#     """
#     matrix = generate_invertible_matrix(
#         0, char_ecncode_mod, len(chars), matrix_seed, char_ecncode_mod
#     )
#     vector = np.array(chars)
#     new_vector = (vector @ matrix) % char_ecncode_mod
#     return new_vector
#
#
# def reverse_change_full_vector_with_matrix(
#     chars: list[int], char_ecncode_mod: int, matrix_seed
# ) -> list[int]:
#     """
#     Decodes a vector that was encoded with `change_full_vector_with_matrix`.
#
#     Args:
#         chars (list[int]): Encoded vector of integers.
#         char_ecncode_mod (int): The modulus for modular arithmetic (must match encoding).
#         matrix_seed (int): The same seed used during encoding (to regenerate the matrix).
#
#     Returns:
#         list[int]: Decoded vector (original input).
#     """
#     matrix = generate_invertible_matrix(
#         0, char_ecncode_mod, len(chars), matrix_seed, char_ecncode_mod
#     )
#     inv_matrix = mod_matrix_inversion(matrix, char_ecncode_mod)
#     vector = np.array(chars)
#     decoded_vector = (vector @ inv_matrix) % char_ecncode_mod
#     return decoded_vector


def change_full_vector_with_matrix(chars: list[int], matrix_seed: int) -> np.ndarray:
    """
    Encodes a vector using a seed-based invertible matrix (no modular arithmetic).
    """
    n = len(chars)
    M = generate_upper_triangular_matrix(n, 1, 258, matrix_seed)
    vector = np.array(chars)
    encoded = vector @ M
    return encoded


def reverse_change_full_vector_with_matrix(
    encoded: list[int], matrix_seed: int
) -> np.ndarray:
    """
    Decodes a vector using the same seed (regenerates the matrix).
    """
    n = len(encoded)
    M = generate_upper_triangular_matrix(n, 1, 258, matrix_seed)
    inv_M = np.linalg.inv(M)  # normal inverse
    decoded = np.rint(encoded @ inv_M).astype(int)  # round back to int
    return decoded


def mod_matrix_inversion(matrix: np.ndarray, mod: int) -> np.ndarray:
    """
    Computes the modular inverse of a square matrix.

    Args:
        matrix (np.ndarray): Square matrix to invert.
        mod (int): Modulus for modular arithmetic.

    Returns:
        np.ndarray: Inverse matrix modulo `mod`.

    Raises:
        ValueError: If the matrix is not invertible modulo `mod`.
    """
    M = Matrix(matrix)
    return np.array(M.inv_mod(mod)).astype(int)


def generate_invertible_matrix(n: int, seed: int) -> np.ndarray:
    """Generate a reproducible random invertible integer matrix using a seed."""
    np.random.seed(seed)
    while True:
        M = np.random.randint(1, 10, size=(n, n))
        if np.linalg.det(M) != 0:  # non-singular
            return M


def generate_upper_triangular_matrix(
    size: int, min_val: int = 1, max_val: int = 10, seed: int | None = None
) -> np.ndarray:
    """
    Generates an upper triangular matrix with constraints:
      - All diagonal elements are odd.
      - First element (0,0) is odd.
      - Second row: diagonal (1,1) and last element (1, size-1) are odd.
      - Elements below the diagonal are zero.

    Args:
        size (int): Dimension of the matrix (size x size).
        min_val (int): Minimum value for random elements (default = 1).
        max_val (int): Maximum value for random elements (default = 10).
        seed (int | None): Random seed for reproducibility (default = None).

    Returns:
        np.ndarray: Generated upper triangular matrix.
    """
    if seed is not None:
        np.random.seed(seed)

    matrix = np.zeros((size, size), dtype=int)

    for i in range(size):
        for j in range(i, size):  # upper triangular part
            val = np.random.randint(min_val, max_val)

            if i == j:  # diagonal must be odd
                if val % 2 == 0:
                    val += 1
            elif i == 0 and j == 0:  # first element odd
                if val % 2 == 0:
                    val += 1
            elif i == 1 and (j == 1 or j == size - 1):  # second row rule
                if val % 2 == 0:
                    val += 1

            matrix[i, j] = val

    return matrix


def main():
    chars = [i for i in range(1000)]
    seed = 122
    mod = 258

    encoded = change_full_vector_with_matrix(chars, seed)
    print("Encoed:", encoded)

    decoded = reverse_change_full_vector_with_matrix(encoded, seed)
    print("Decoded:", decoded)


if __name__ == "__main__":
    main()
