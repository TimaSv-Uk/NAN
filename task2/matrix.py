import numpy as np
from sympy import Matrix
import time


def matrix_vector_mult(matrix, vector):
    new_vector = []
    for row in matrix:
        sum = 0
        for index, item in enumerate(row):
            sum += item * vector[index]
        new_vector.append(sum)
    return new_vector


def vector_matrix_mult(vector, matrix):
    new_vector = []

    for i in range(len(vector)):
        sum = 0
        for j in range(len(matrix[i])):
            sum += vector[j] * matrix[j][i]
        new_vector.append(sum)
    return new_vector


# TODO: assignment6
def change_full_vector_with_matrix(
    chars: np.ndarray, matrix_seed: int, mod: int = 256
) -> np.ndarray:
    """
    Encodes a vector using a seed-based invertible matrix (no modular arithmetic).
    """
    n = len(chars)
    M = generate_upper_triangular_matrix_of_bytes(n, matrix_seed)
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

    inv_M = mod_matrix_inversion(M, mod)
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

    # for i in range(size):
    #     for j in range(i + 1, size):
    #         val = np.random.randint(1, 256)
    #         if val % 2 == 0:
    #             val += 1
    #             if val > 255:
    #                 val -= 2
    #         matrix[i, j] = val

    for i in range(1, size):
        val = np.random.randint(1, 256)
        if val % 2 == 0:
            val += 1
            if val > 255:
                val -= 2
        matrix[0, i] = val
    return matrix


def main():
    mod = 256
    chars = np.random.randint(1, mod - 1, size=10, dtype=int)
    # chars = np.array([3, 4, 5, 7, 23, 23, 3], dtype=int)
    seed = 42

    M = generate_upper_triangular_matrix_of_bytes(len(chars), seed)
    inv_M = mod_matrix_inversion(M, mod)

    encoded = (chars @ M) % mod
    decoded = (encoded @ inv_M) % mod

    print(M)
    print(inv_M)

    encoded = change_full_vector_with_matrix(chars, seed, mod)
    decode = reverse_change_full_vector_with_matrix(encoded, seed, mod)
    print(chars)
    print(encoded)
    print(decode)
    print(np.all(decoded == chars))  # should print True

if __name__ == "__main__":
    main()
