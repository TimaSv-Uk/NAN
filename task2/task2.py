from sympy import Matrix
import numpy as np
from numba import njit
from precompute_multiplication import read_precompute_multiplication


# NOTE:
# np.uint8 used inted of  modulo operation only works with  mod 256

# NOTE:
# val = (x * y) & mod  # instead of % 256, only works if your modulus is a power of two


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

    current_state = chars.copy().astype(np.uint8)
    # current_state = chars.copy()
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

    current_state = chars.copy().astype(np.uint8)
    # current_state = chars.copy()
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
            point_out[i] = np.uint8(point_in[i] - point_out[0] * point_in[i - 1])
            # point_out[i] = temp % mod
            # point_out[i] = temp & mod
        else:
            point_out[i] = np.uint8(point_in[i] - x0 * point_out[i - 1])
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


# TODO: assignment6


def change_full_vector_with_matrix(
    chars: np.ndarray, matrix_seed: int, mod: int = 256
) -> np.ndarray:
    """
    Encodes a vector using a seed-based invertible matrix (no modular arithmetic).
    """
    n = len(chars)
    M = generate_upper_triangular_matrix_of_bytes(n, matrix_seed)
    print(M)
    encoded = (chars @ M) % mod

    return encoded


def reverse_change_full_vector_with_matrix(
    encoded: np.ndarray, matrix_seed: int, mod: int = 256
) -> np.ndarray:
    """
    Decodes a vector using the same seed (regenerates the matrix).
    """
    n = len(encoded)
    M = generate_upper_triangular_matrix_of_bytes(n, matrix_seed)
    print(M)

    inv_M = invert_upper_triangular_mod(M, mod)
    decoded = (encoded @ inv_M) % mod
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


def generate_upper_triangular_matrix_of_bytes(
    size: int, seed: int | None = None
) -> np.ndarray:
    """
    Generate an upper triangular matrix with:
      - Diagonal elements are 1.
      - Elements below diagonal are 0.

    Args:
        size (int): Matrix size (size x size).
        seed (int | None): Random seed for reproducibility.

    Returns:
        np.ndarray: The generated matrix (dtype=uint8).
    """
    if seed is not None:
        np.random.seed(seed)

    matrix = np.zeros((size, size), int)

    # Set diagonal elements to 1
    np.fill_diagonal(matrix, 1)

    # all rows above the diagonal non-zero random odd numbers

    for i in range(size):
        for j in range(i + 1, size):
            val = np.random.randint(1, 256)
            if val % 2 == 0:
                val += 1
                if val > 255:
                    val -= 2
            matrix[i, j] = val
    #
    return matrix


# TODO:
def invert_upper_triangular_mod(M, mod=256):
    return M


def main():
    # chars = np.array([i for i in range(100)], int)
    #
    # seed = 42
    # mod = 256
    # encoded = change_full_vector_with_matrix(chars, seed)
    # decode = reverse_change_full_vector_with_matrix(encoded, seed)
    # print(chars)
    # print(encoded)
    # print(decode)
    mod = 256
    chars = np.arange(100, dtype=int)
    seed = 42

    M = generate_upper_triangular_matrix_of_bytes(len(chars), seed)
    inv_M = invert_upper_triangular_mod(M, mod)

    encoded = (chars @ M) % mod
    decoded = (encoded @ inv_M) % mod

    print(np.all(decoded == chars))  # should print True


if __name__ == "__main__":
    main()
