import numpy as np
from numba import njit


def encode_f8(
    chars: np.ndarray, d_mod_range: np.ndarray
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
        find_neighbors_f8(current_state, next_state, a)

        current_state, next_state = next_state, current_state

    return current_state


def decode_f8(
    chars: np.ndarray, d_mod_range: np.ndarray
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
        reverse_find_neighbors_f8(current_state, next_state, a)
        current_state, next_state = next_state, current_state  # Swap

    return current_state


# @njit
def g_mul(a, b):
    """Galois Field GF(2^8) multiplication."""
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


# @njit
def find_neighbors_f8(point_in: np.ndarray, point_out: np.ndarray, a: int) -> None:
    """
    point_in  = (x0, x1, x2, ...)
    Calculates Y node from X in GF(2^8)^n
    """
    n = len(point_in)

    # y0 = x0 + a (In GF2^8, addition is XOR)
    point_out[0] = point_in[0] ^ a

    x0 = point_in[0]
    y0 = point_out[0]

    for i in range(1, n):
        if i % 2 == 0:
            # Even index: y_i = x_i - (y0 * x_{i-1})
            # Subtraction is XOR; Multiplication is g_mul
            prod = g_mul(y0, point_in[i - 1])
            point_out[i] = point_in[i] ^ prod
        else:
            # Odd index: y_i = x_i - (x0 * y_{i-1})
            prod = g_mul(x0, point_out[i - 1])
            point_out[i] = point_in[i] ^ prod


# @njit
def reverse_find_neighbors_f8(
    point_in: np.ndarray, point_out: np.ndarray, a: int
) -> None:
    """
    point_in  = [y0, y1, y2, ...] (Y node)
    point_out = [x0, x1, x2, ...] (X node)

    Reverse transformation in GF(2^8)
    """
    n = len(point_in)

    # x0 = y0 - a -> In GF(2^8), this is y0 ^ a
    point_out[0] = point_in[0] ^ a

    x0 = point_out[0]  # x1 in your math notation
    y0 = point_in[0]  # y1 in your math notation

    for i in range(1, n):
        if i % 2 == 0:
            # Even index (math i=3, 5...): x_i = y_i + y1 * x_{i-1}
            prod = g_mul(y0, point_out[i - 1])
            point_out[i] = point_in[i] ^ prod
        else:
            # Odd index (math i=2, 4...): x_i = y_i + x1 * y_{i-1}
            prod = g_mul(x0, point_in[i - 1])
            point_out[i] = point_in[i] ^ prod

