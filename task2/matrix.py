import numpy as np
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



# TODO: assignment6 draft

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
#
#
# def change_full_vector_with_matrix(chars: list[int], matrix_seed: int) -> np.ndarray:
#     """
#     Encodes a vector using a seed-based invertible matrix (no modular arithmetic).
#     """
#     n = len(chars)
#     M = generate_upper_triangular_matrix(n, 1, 258, matrix_seed)
#     vector = np.array(chars)
#     encoded = vector @ M
#     return encoded
#
#
# def reverse_change_full_vector_with_matrix(
#     encoded: list[int], matrix_seed: int
# ) -> np.ndarray:
#     """
#     Decodes a vector using the same seed (regenerates the matrix).
#     """
#     n = len(encoded)
#     M = generate_upper_triangular_matrix(n, 1, 258, matrix_seed)
#     inv_M = np.linalg.inv(M)  # normal inverse
#     decoded = np.rint(encoded @ inv_M).astype(int)  # round back to int
#     return decoded
#
#
# def mod_matrix_inversion(matrix: np.ndarray, mod: int) -> np.ndarray:
#     """
#     Computes the modular inverse of a square matrix.
#
#     Args:
#         matrix (np.ndarray): Square matrix to invert.
#         mod (int): Modulus for modular arithmetic.
#
#     Returns:
#         np.ndarray: Inverse matrix modulo `mod`.
#
#     Raises:
#         ValueError: If the matrix is not invertible modulo `mod`.
#     """
#     M = Matrix(matrix)
#     return np.array(M.inv_mod(mod)).astype(int)
#
#
# def generate_invertible_matrix(n: int, seed: int) -> np.ndarray:
#     """Generate a reproducible random invertible integer matrix using a seed."""
#     np.random.seed(seed)
#     while True:
#         M = np.random.randint(1, 10, size=(n, n))
#         if np.linalg.det(M) != 0:  # non-singular
#             return M
# def generate_upper_triangular_matrix(
#     size: int, min_val: int = 1, max_val: int = 10, seed: int | None = None
# ) -> np.ndarray:
#     """
#     Generates an upper triangular matrix with constraints:
#       - All diagonal elements are odd.
#       - First element (0,0) is odd.
#       - Second row: diagonal (1,1) and last element (1, size-1) are odd.
#       - Elements below the diagonal are zero.
#
#     Args:
#         size (int): Dimension of the matrix (size x size).
#         min_val (int): Minimum value for random elements (default = 1).
#         max_val (int): Maximum value for random elements (default = 10).
#         seed (int | None): Random seed for reproducibility (default = None).
#
#     Returns:
#         np.ndarray: Generated upper triangular matrix.
#     """
#     if seed is not None:
#         np.random.seed(seed)
#
#     matrix = np.zeros((size, size), dtype=int)
#
#     for i in range(size):
#         for j in range(i, size):  # upper triangular part
#             val = np.random.randint(min_val, max_val)
#
#             if i == j:  # diagonal must be odd
#                 if val % 2 == 0:
#                     val += 1
#             elif i == 0 and j == 0:  # first element odd
#                 if val % 2 == 0:
#                     val += 1
#             elif i == 1 and (j == 1 or j == size - 1):  # second row rule
#                 if val % 2 == 0:
#                     val += 1
#
#             matrix[i, j] = val
#
#     return matrix

def main():
    # chars = [i for i in range(10)]
    # seed = 42
    # mod = 258
    # shape (3,) works like a column vector here
    vector = [3, 1, 2]
    matrix = [[1, 1, 2], [2, 1, 3], [1, 4, 2]]

    start_time = time.perf_counter()
    print(matrix_vector_mult(matrix, vector))
    print(vector_matrix_mult(vector, matrix))
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    print(execution_time)

    vector = np.array([3, 1, 2])
    matrix = np.array([[1, 1, 2], [2, 1, 3], [1, 4, 2]])
    start_time = time.perf_counter()
    print((matrix @ vector) % 2)
    print((vector @ matrix) % 2)
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    print(execution_time)


if __name__ == "__main__":
    main()
