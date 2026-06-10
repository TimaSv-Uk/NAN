import numpy as np
from numba import njit


from ..precompute_multiplication import load_sudo512_mod

MUL_SUDO512_MOD = load_sudo512_mod("multiplication_table/mod_256_sudo512.npy")


@njit
def encode_sudo512_mod(
    chars: np.ndarray, d_mod_range: np.ndarray, mul_lut: np.ndarray = MUL_SUDO512_MOD
) -> np.ndarray:
    # Use standard uint8 arrays

    current_state = (chars.astype(np.uint16) * 2) + 1

    next_state = np.zeros_like(current_state)

    for a in d_mod_range:
        a = np.uint16((2 * a) + 1)
        find_neighbors_sudo512_mod(current_state, next_state, a, mul_lut)

        temp = current_state
        current_state = next_state
        next_state = temp

    # Reverse Mapping (Modulo 512 to Byte)
    current_state = ((current_state - 1) // 2).astype(np.uint8)
    return current_state


@njit
def decode_sudo512_mod(
    chars: np.ndarray, d_mod_range: np.ndarray, mul_lut: np.ndarray = MUL_SUDO512_MOD
) -> np.ndarray:

    current_state = (chars.astype(np.uint16) * 2) + 1

    next_state = np.zeros_like(current_state)

    for i in range(len(d_mod_range) - 1, -1, -1):
        a = np.uint16((2 * d_mod_range[i]) + 1)

        reverse_find_neighbors_sudo512_mod(current_state, next_state, a, mul_lut)

        temp = current_state
        current_state = next_state
        next_state = temp

    # Reverse Mapping (Modulo 512 to Byte)
    current_state = ((current_state - 1) // 2).astype(np.uint8)

    return current_state


@njit
def find_neighbors_sudo512_mod(
    point_in: np.ndarray, point_out: np.ndarray, a: np.uint16, mul_lut: np.ndarray
) -> None:
    """
    Encoding neighbor step in Z512 odd subgroup.

    Graph rule (multiplicative):
      y1     = x1 * a          (mod 512)
      y_even = x_i - y1 * x_{i-1}   (mod 512, subtraction = inverse mul? No — use additive)
      ...

    y1 = x1 * a  (mod 512)   <- multiplicative shift
    even i: y_i = x_i - (y1 * x_{i-1})  mod 512
    odd  i: y_i = x_i - (x1 * y_{i-1})  mod 512
    All values are ODD (in the odd coset), subtraction wraps in uint16 then % 512.

    """
    n = len(point_in)

    # y1 = x1 * a  (multiplicative shift, stays odd)
    point_out[0] = (point_in[0] * a) % 512
    x0 = point_in[0]  # x1 (odd, uint16)
    y0 = point_out[0]  # y1 (odd, uint16)

    for i in range(1, n):
        xi = point_in[i]

        # NOTE: Adding 512 before % 512 is a trick to keep the value positive:
        # (3 - 7 + 512) % 512 = 508   correct negative wrap in Z512
        # (3 - 7)       % 512 = ???   uint16 underflow before % even runs
        if i % 2 == 0:
            # even math index: y_i = x_i - (y1 * x_{i-1})  mod 512
            mul = mul_lut[y0 // 2, point_in[i - 1] // 2]
            point_out[i] = (xi - mul + 512) % 512
        else:
            # odd math index:  y_i = x_i - (x1 * y_{i-1})  mod 512
            mul = mul_lut[x0 // 2, point_out[i - 1] // 2]
            point_out[i] = (xi - mul + 512) % 512


@njit
def reverse_find_neighbors_sudo512_mod(
    point_in: np.ndarray, point_out: np.ndarray, a: np.uint16, mul_lut: np.ndarray
) -> None:
    """
    Decoding neighbor step. Inverse of find_neighbors_sudo512_mod.

    x1 = y1 * a^{-1}  mod 512   (multiplicative inverse of a in Z512*)
    even i: x_i = y_i + (y1 * x_{i-1})  mod 512
    odd  i: x_i = y_i + (x1 * y_{i-1})  mod 512

    NOTE: a is always odd (passed as 2*d+1), so it has a multiplicative
    inverse in Z512. We compute it once per call.
    """
    n = len(point_in)

    # Compute modular inverse of a in Z512 (a is odd, so gcd(a,512)=1)
    a_inv = np.uint16(_mod_inverse_512(a))

    # x1 = y1 * a_inv  mod 512
    point_out[0] = (point_in[0] * a_inv) % 512
    x0 = point_out[0]
    y0 = point_in[0]

    for i in range(1, n):
        yi = point_in[i]
        if i % 2 == 0:
            # even: x_i = y_i + (y1 * x_{i-1})  mod 512
            mul = mul_lut[y0 // 2, point_out[i - 1] // 2]
            point_out[i] = (yi + mul) % 512
        else:
            # odd:  x_i = y_i + (x1 * y_{i-1})  mod 512
            mul = mul_lut[x0 // 2, point_in[i - 1] // 2]
            point_out[i] = (yi + mul) % 512


@njit
def _mod_inverse_512(a: np.uint16) -> np.uint16:
    """Extended Euclidean: returns x s.t. a*x ≡ 1 (mod 512).
    Only valid when a is odd (gcd(a,512)=1)."""
    MOD = np.int32(512)
    old_r, r = np.int32(a), MOD
    old_s, s = np.int32(1), np.int32(0)
    while r != 0:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
    return np.uint16(old_s % MOD)
