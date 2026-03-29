import numpy as np
from numba import njit


from ..precompute_multiplication import load_gf256

MUL_GF256 = load_gf256("multiplication_table/mul_gf256.npy")


@njit
def encode_f8(
    chars: np.ndarray, d_mod_range: np.ndarray, mul_lut: np.ndarray = MUL_GF256
) -> np.ndarray:
    # Use standard uint8 arrays
    current_state = chars.astype(np.uint8)
    next_state = np.zeros_like(current_state)

    for a in d_mod_range:
        find_neighbors_f8(current_state, next_state, np.uint8(a), mul_lut)

        temp = current_state
        current_state = next_state
        next_state = temp

    return current_state


@njit
def decode_f8(
    chars: np.ndarray, d_mod_range: np.ndarray, mul_lut: np.ndarray = MUL_GF256
) -> np.ndarray:
    current_state = chars.astype(np.uint8)
    next_state = np.zeros_like(current_state)

    for i in range(len(d_mod_range) - 1, -1, -1):
        a = np.uint8(d_mod_range[i])
        reverse_find_neighbors_f8(current_state, next_state, a, mul_lut)

        temp = current_state
        current_state = next_state
        next_state = temp

    return current_state


@njit
def find_neighbors_f8(
    point_in: np.ndarray, point_out: np.ndarray, a: int, mul_lut: np.ndarray
) -> None:
    n = len(point_in)

    # y0 = x0 + a -> Addition is XOR (^)
    point_out[0] = point_in[0] ^ a

    x0 = point_in[0]
    y0 = point_out[0]

    for i in range(1, n):
        if i % 2 == 0:
            # y_i = x_i + (y0 * x_{i-1})
            # Multiplication is a lookup: mul_lut[y0, x_{i-1}]
            point_out[i] = point_in[i] ^ mul_lut[y0, point_in[i - 1]]
        else:
            # y_i = x_i + (x0 * y_{i-1})
            point_out[i] = point_in[i] ^ mul_lut[x0, point_out[i - 1]]


@njit
def reverse_find_neighbors_f8(
    point_in: np.ndarray, point_out: np.ndarray, a: int, mul_lut: np.ndarray
) -> None:
    n = len(point_in)

    # x0 = y0 - a -> Subtraction is also XOR (^)
    point_out[0] = point_in[0] ^ a

    x0 = point_out[0]
    y0 = point_in[0]

    for i in range(1, n):
        if i % 2 == 0:
            # x_i = y_i + (y0 * x_{i-1})
            point_out[i] = point_in[i] ^ mul_lut[y0, point_out[i - 1]]
        else:
            # x_i = y_i + (x0 * y_{i-1})
            point_out[i] = point_in[i] ^ mul_lut[x0, point_in[i - 1]]
