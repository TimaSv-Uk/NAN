import numpy as np
import galois
from numba import njit

@njit
def g_mul(a, b):
    """Galois Field GF(2^8) multiplication."""
    """I desided to use librari insted of my own frigile implementation"""
    p = 0
    for i in range(8):
        if (b & 1) != 0:
            p ^= a
        hi_bit_set = (a & 0x80) != 0
        a <<= 1
        if hi_bit_set:
            # The irreducible polynomial for AES (x^8 + x^4 + x^3 + x + 1)
            a ^= 0x1B
        b >>= 1
    return p & 0xFF


# Initialize the Galois Field for GF(2^8)
GF256 = galois.GF(2**8)


def encode_f8(chars: np.ndarray, d_mod_range: np.ndarray) -> np.ndarray:
    """
    Transforms the input vector X into Y using the specified formulas in GF(2^8).
    """
    # Convert inputs to Galois Field arrays
    current_state = GF256(chars.astype(np.uint8))
    next_state = GF256.Zeros(current_state.shape)

    for a in d_mod_range:
        find_neighbors_f8(current_state, next_state, int(a))
        # Swap states
        current_state, next_state = next_state, current_state

    # Return as standard numpy uint8 array
    return np.array(current_state, dtype=np.uint8)


def decode_f8(chars: np.ndarray, d_mod_range: np.ndarray) -> np.ndarray:
    """
    Reverses the transformation from Y back to X in GF(2^8).
    """
    current_state = GF256(chars.astype(np.uint8))
    next_state = GF256.Zeros(current_state.shape)

    # Backward range
    for i in range(len(d_mod_range) - 1, -1, -1):
        a = int(d_mod_range[i])
        reverse_find_neighbors_f8(current_state, next_state, a)
        # Swap states
        current_state, next_state = next_state, current_state

    return np.array(current_state, dtype=np.uint8)


def find_neighbors_f8(
    point_in: galois.FieldArray, point_out: galois.FieldArray, a: int
) -> None:
    """
    Calculates Y node from X in GF(2^8)^n
    """
    a_gf = GF256(a)
    n = len(point_in)

    # y0 = x0 + a (In GF(2^8), + maps to XOR)
    point_out[0] = point_in[0] + a_gf

    x0 = point_in[0]
    y0 = point_out[0]

    for i in range(1, n):
        if i % 2 == 0:
            # Even index: y_i = x_i + (y0 * x_{i-1})
            point_out[i] = point_in[i] + (y0 * point_in[i - 1])
        else:
            # Odd index: y_i = x_i + (x0 * y_{i-1})
            point_out[i] = point_in[i] + (x0 * point_out[i - 1])


def reverse_find_neighbors_f8(
    point_in: galois.FieldArray, point_out: galois.FieldArray, a: int
) -> None:
    """
    Reverse transformation in GF(2^8) from Y node to X node
    """
    a_gf = GF256(a)
    n = len(point_in)

    # x0 = y0 - a -> In GF(2^8), subtraction is the same as addition (XOR)
    point_out[0] = point_in[0] + a_gf

    x0 = point_out[0]
    y0 = point_in[0]

    for i in range(1, n):
        if i % 2 == 0:
            # Even index: x_i = y_i + (y0 * x_{i-1})
            point_out[i] = point_in[i] + (y0 * point_out[i - 1])
        else:
            # Odd index: x_i = y_i + (x0 * y_{i-1})
            point_out[i] = point_in[i] + (x0 * point_in[i - 1])
