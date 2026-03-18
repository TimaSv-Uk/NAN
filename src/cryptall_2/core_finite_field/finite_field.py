import numpy as np
from numba import njit


@njit
def g_mul(a: int, b: int) -> int:
    """Multiplies two numbers in GF(2^8) using the default polynomial 0x11B."""
    p = 0
    for _ in range(8):
        if b & 1:
            p ^= a
        hi_bit_set = a & 0x80
        a = (a << 1) & 0xFF
        if hi_bit_set:
            a ^= 0x1B  # The irreducible polynomial without the 9th bit
        b >>= 1
    return p


def encode_f8(chars: np.ndarray, d_mod_range: np.ndarray) -> np.ndarray:
    """
    Transforms the input vector X into Y using the specified formulas in GF(2^8).
    """
    # Convert inputs to Galois Field arrays
    current_state = chars.astype(np.uint8).copy()
    next_state = np.empty_like(current_state)

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
    current_state = chars.astype(np.uint8).copy()
    next_state = np.empty_like(current_state)

    # Backward range
    for i in range(len(d_mod_range) - 1, -1, -1):
        a = int(d_mod_range[i])
        reverse_find_neighbors_f8(current_state, next_state, a)
        # Swap states
        current_state, next_state = next_state, current_state

    return np.array(current_state, dtype=np.uint8)


@njit
def find_neighbors_f8(point_in, point_out, a):
    n = len(point_in)

    # y0 = x0 + a (In GF(2^8), + maps to XOR)
    point_out[0] = point_in[0] ^ a

    x0 = point_in[0]
    y0 = point_out[0]

    for i in range(1, n):
        if i % 2 == 0:
            # Even index: y_i = x_i + (y0 * x_{i-1})
            point_out[i] = point_in[i] ^ g_mul(y0, point_in[i - 1])
        else:
            # Odd index: y_i = x_i + (x0 * y_{i-1})
            point_out[i] = point_in[i] ^ g_mul(x0, point_out[i - 1])




@njit
def reverse_find_neighbors_f8(point_in, point_out, a):
    n = len(point_in)

    # x0 = y0 - a -> In GF(2^8), subtraction is the same as addition (XOR)
    point_out[0] = point_in[0] ^ a

    x0 = point_out[0]
    y0 = point_in[0]

    for i in range(1, n):
        if i % 2 == 0:
            # Even index: x_i = y_i + (y0 * x_{i-1})
            point_out[i] = point_in[i] ^ g_mul(y0, point_out[i - 1])
        else:
            # Odd index: x_i = y_i + (x0 * y_{i-1})
            point_out[i] = point_in[i] ^ g_mul(x0, point_in[i - 1])
