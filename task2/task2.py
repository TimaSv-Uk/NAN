from sympy import Matrix
import numpy as np


def encode(encoded_text_int: list[int], char_ecncode_mod: int, d_mod: int) -> list[int]:
    chars = encoded_text_int.copy()
    for a in range(d_mod):
        if a % 2 == 0:
            chars = find_neigbors_N_a(chars, a, char_ecncode_mod)
        else:
            chars = find_neigbors_M_a(chars, a, char_ecncode_mod)
    return chars


def decode(encoded_text_int: list[int], char_ecncode_mod: int, d_mod: int) -> list[int]:
    chars = encoded_text_int.copy()
    for a in reversed(range(d_mod)):
        if a % 2 == 0:
            chars = reverce_find_neigbors_N_a(chars, a, char_ecncode_mod)
            # print(f"After reverse N_a({a}): {chars}")
        else:
            chars = reverce_find_neigbors_M_a(chars, a, char_ecncode_mod)
            # print(f"After reverse M_a({a}): {chars}")
    return chars


def find_neigbors_N_a(point, a, mod):
    """
    # N_a(X) = [x1+a, z2, z3, ..., zn]
    # де:
    # z2 = x1 * (x1 + a) - x2
    # z3 = x1 * z2 - x3
    # ...,
    # zn = x1 * z(n-1) - xn
    """
    point = point.copy()
    neigbor_point = []

    for i, coord in enumerate(point):
        if i == 0:
            x1 = (point[0] + a) % mod
            neigbor_point.append(x1)
        elif i == 1:
            z2 = (point[0] * (point[0] + a) - point[i]) % mod
            neigbor_point.append(z2)
        else:
            z_i = (point[0] * neigbor_point[-1] - point[i]) % mod
            neigbor_point.append(z_i)
    return neigbor_point


def find_neigbors_M_a(point, a, mod):
    """
    # M_a(X) = [y1+a, z2, z3, ..., zn]
    # де:
    # z2 = y1 * (y1 + a) - x2
    # z3 = (y1 + a) * z2 - x3
    """
    point = point.copy()
    neigbor_point = []

    for i, coord in enumerate(point):
        if i == 0:
            y1 = (point[0] + a) % mod
            neigbor_point.append(y1)
        elif i == 1:
            z2 = (point[0] * (point[0] + a) - point[i]) % mod
            neigbor_point.append(z2)
        else:
            z_i = ((point[0] + a) * neigbor_point[-1] - point[i]) % mod
            neigbor_point.append(z_i)
    return neigbor_point


# NOTE: decode
# n від - as
# n - a1
# M as-1
# last step N - a1
def reverce_find_neigbors_N_a(point, a, mod):
    """
    # Reverse of N_a(X) = [x1+a, z2, z3, ..., zn]
    # where:
    # z2 = x1 * (x1 + a) - x2  =>  x2 = x1 * (x1 + a) - z2
    # z3 = x1 * z2 - x3  =>  x3 = x1 * z2 - z3
    # ...
    # zn = x1 * z(n-1) - xn  =>  xn = x1 * z(n-1) - zn
    """
    point = point.copy()
    original_point = []

    for i in range(len(point)):
        if i == 0:
            x1 = (point[0] - a) % mod
            original_point.append(x1)
        elif i == 1:
            x2 = (original_point[0] * (original_point[0] + a) - point[i]) % mod
            original_point.append(x2)
        else:
            xi = (original_point[0] * point[i - 1] - point[i]) % mod
            original_point.append(xi)
    return original_point


def reverce_find_neigbors_M_a(point, a, mod):
    # Reverse of M_a(X) = [y1+a, z2, z3, ..., zn]
    # where:
    # z2 = y1 * (y1 + a) - x2  =>  x2 = y1 * (y1 + a) - z2
    # z3 = (y1 + a) * z2 - x3  =>  x3 = (y1 + a) * z2 - z3
    # ...
    # zn = (y1 + a) * z(n-1) - xn  =>  xn = (y1 + a) * z(n-1) - zn

    point = point.copy()
    original_point = []

    for i in range(len(point)):
        if i == 0:
            # x1 = z1 - a
            x1 = (point[0] - a) % mod
            original_point.append(x1)
        elif i == 1:
            # x2 = x1 * (x1 + a) - z2
            x2 = (original_point[0] * (original_point[0] + a) - point[i]) % mod
            original_point.append(x2)
        else:
            # xi = (x1 + a) * z(i-1) - zi
            xi = ((original_point[0] + a) * point[i - 1] - point[i]) % mod
            original_point.append(xi)
    return original_point


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


def encode_assignment5(
    encoded_text_int: list[int], char_ecncode_mod: int, d_mod: int
) -> list[int]:
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
    chars = encoded_text_int.copy()
    # print(encoded_text_int)
    for a in range(d_mod):
        # prev_chars = chars.copy()
        chars = find_neighbors_assignment5(chars, a, char_ecncode_mod)
        # print(follows_graph_rule_assignment5(prev_chars, chars, d_mod))
        print(chars)
    return chars


def decode_assignment5(
    encoded_text_int: list[int], char_ecncode_mod: int, d_mod: int
) -> list[int]:
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
    chars = encoded_text_int.copy()
    # print(encoded_text_int)
    for a in reversed(range(d_mod)):
        # prev_chars = chars.copy()
        chars = reverse_find_neighbors_assignment5(chars, a, char_ecncode_mod)
        # print(follows_graph_rule_assignment5(prev_chars, chars, d_mod))
        print(chars)
    return chars


def find_neighbors_assignment5(point, a, mod):
    """
    point = (x1, x2, x3, ...)
    get Y node from X

    # index 1: y1 = x1 + a
    # even math index: y_i = x_i - (y1 * x_{i-1})
    # odd math index: y_i = x_i - (x1 * y_{i-1})

    """
    point = point.copy()
    neighbor_point = []

    for i in range(len(point)):
        if i == 0:
            # math index 1: y1 = x1 + a
            y1 = (point[0] + a) % mod
            neighbor_point.append(y1)
        elif i % 2 == 0:
            # even math index: y_i = x_i - (y1 * x_{i-1})
            y_i = (point[i] - (neighbor_point[0] * point[i - 1])) % mod
            neighbor_point.append(y_i)
        else:
            # odd math index: y_i = x_i - (x1 * y_{i-1})
            y_i = (point[i] - (point[0] * neighbor_point[i - 1])) % mod
            neighbor_point.append(y_i)
    return neighbor_point


def reverse_find_neighbors_assignment5(point, a, mod):
    """
    point = [y1, y2, y3, ...]
    get X node from Y

    # index 1: x1 = y1 - a
    # even math index: x_i = y_i + y1 * x_{i-1}
    # odd math index: x_i = y_i + x1 * y_{i-1}

    """
    point = point.copy()
    neighbor_point = []

    for i in range(len(point)):
        if i == 0:
            # x1 = y1 - a
            x1 = (point[0] - a) % mod
            neighbor_point.append(x1)
        elif i % 2 == 0:
            # even math index x_i = y_i + y1 * x_{i-1}
            x_i = (point[i] + (point[0] * neighbor_point[i - 1])) % mod
            neighbor_point.append(x_i)
        else:
            # odd math index x_i = y_i + x1 * y_{i-1}
            x_i = (point[i] + (neighbor_point[0] * point[i - 1])) % mod
            neighbor_point.append(x_i)
    return neighbor_point


# TODO: assignment6


# TODO: assignment6
def change_full_vector_with_matrix(
    chars: list[int], char_ecncode_mod: int, matrix_seed
) -> list[int]:
    """
    Encodes a vector using a randomly generated invertible matrix (modular arithmetic).

    Args:
        chars (list[int]): Input vector of integers to encode.
        char_ecncode_mod (int): The modulus for modular arithmetic (e.g. 258).
        matrix_seed (int): Seed for the random generator to ensure reproducibility.

    Returns:
        list[int]: Encoded vector (same length as input).
    """
    matrix = generate_invertible_matrix(
        1, 10, len(chars), matrix_seed, char_ecncode_mod
    )
    vector = np.array(chars)
    new_vector = (matrix @ vector) % char_ecncode_mod
    return new_vector


def reverse_change_full_vector_with_matrix(
    chars: list[int], char_ecncode_mod: int, matrix_seed
) -> list[int]:
    """
    Decodes a vector that was encoded with `change_full_vector_with_matrix`.

    Args:
        chars (list[int]): Encoded vector of integers.
        char_ecncode_mod (int): The modulus for modular arithmetic (must match encoding).
        matrix_seed (int): The same seed used during encoding (to regenerate the matrix).

    Returns:
        list[int]: Decoded vector (original input).
    """
    matrix = generate_invertible_matrix(
        1, 10, len(chars), matrix_seed, char_ecncode_mod
    )
    inv_matrix = mod_matrix_inversion(matrix, char_ecncode_mod)
    vector = np.array(chars)
    decoded_vector = (inv_matrix @ vector) % char_ecncode_mod
    return decoded_vector


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


def generate_matrix(min_val: int, max_val: int, size: int, seed: int) -> np.ndarray:
    """
    Generates a random square matrix with integer entries.

    Args:
        min_val (int): Minimum value for entries.
        max_val (int): Maximum value for entries.
        size (int): Dimension of the matrix (size x size).
        seed (int): Random seed for reproducibility.

    Returns:
        np.ndarray: Randomly generated square matrix.
    """
    np.random.seed(seed)
    matrix = np.random.randint(min_val, max_val, (size, size))
    return matrix


def generate_invertible_matrix(
    min_val: int, max_val: int, size: int, seed: int, mod: int
) -> np.ndarray:
    """
    Generates a random invertible square matrix modulo `mod`.

    Keeps generating random matrices until one is found
    whose determinant is nonzero modulo `mod` and coprime with `mod`.

    Args:
        min_val (int): Minimum value for entries.
        max_val (int): Maximum value for entries.
        size (int): Dimension of the matrix (size x size).
        seed (int): Random seed for reproducibility.
        mod (int): Modulus for modular arithmetic.

    Returns:
        np.ndarray: Invertible square matrix modulo `mod`.
    """
    np.random.seed(seed)
    while True:
        matrix = np.random.randint(min_val, max_val, (size, size))
        M = Matrix(matrix)
        if M.det() % mod != 0 and np.gcd(int(M.det()), mod) == 1:
            return matrix


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
    chars = [i for i in range(10)]
    seed = 42
    mod = 258

    encoded = change_full_vector_with_matrix(chars, mod, seed)
    print("Encoed:", encoded)

    decoded = reverse_change_full_vector_with_matrix(encoded, mod, seed)
    print("Decoded:", decoded)


if __name__ == "__main__":
    main()
