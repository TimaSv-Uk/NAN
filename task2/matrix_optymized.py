import numpy as np


def generate_first_row_of_matrix(size: int, seed: int) -> np.ndarray:
    """
    Generate the first row of the custom upper triangular matrix.
    All numbers are odd integers between 1 and 255.
    """

    row = np.random.randint(1, 256, size=size, dtype=int)
    # Make all numbers odd
    row = np.where(row % 2 == 0, row + 1, row)
    row = np.where(row > 255, row - 2, row)
    return row


def modular_inverse_odd(a: int, mod: int = 256) -> int:
    """
    Compute modular inverse of an odd number 'a' under 'mod'.
    """
    return pow(int(a), -1, mod)


def change_full_vector_with_matrix(
    chars: np.ndarray, matrix_seed: int, mod: int = 256
) -> np.ndarray:
    """
    Encodes a vector using a seed-based pseudo-matrix (only first row used).
    """
    pass


def reverse_change_full_vector_with_matrix(
    encoded: np.ndarray, matrix_seed: int, mod: int = 256
) -> np.ndarray:
    """
    Decodes a vector encoded with `change_full_vector_with_matrix`.
    """
    pass


def main():
    mod = 256
    size = 10000000
    chars = np.random.randint(1, mod, size=10, dtype=int)
    seed = 42


if __name__ == "__main__":
    main()
