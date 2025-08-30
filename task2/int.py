import numpy as np
from numba import njit, prange
import numba


@njit(parallel=True)
def encode_assignment5_vectorized(chars: np.ndarray, char_encode_mod: int, d_mod: int):
    """Vectorized version using parallel processing"""
    current_state = chars.copy()

    for a in range(d_mod):
        # Vectorized first element calculation
        y1 = (current_state[0] + a) % char_encode_mod
        x1 = current_state[0]

        # Create new state array
        new_state = np.empty_like(current_state)
        new_state[0] = y1

        # Vectorized even indices (i % 2 == 0, i > 0)
        even_indices = np.arange(2, len(current_state), 2)
        if len(even_indices) > 0:
            new_state[even_indices] = (
                current_state[even_indices] - y1 * current_state[even_indices - 1]
            ) % char_encode_mod

        # Vectorized odd indices (i % 2 == 1)
        odd_indices = np.arange(1, len(current_state), 2)
        if len(odd_indices) > 0:
            # For odd indices, we need the previous y value
            for i in odd_indices:
                new_state[i] = (
                    current_state[i] - x1 * new_state[i - 1]
                ) % char_encode_mod

        current_state = new_state

    return current_state


@njit
def encode_assignment5_optimized(chars: np.ndarray, char_encode_mod: int, d_mod: int):
    """Optimized version without table lookup"""
    current_state = chars.copy()
    next_state = np.empty_like(current_state)

    for a in range(d_mod):
        find_neighbors_assignment5_optimized(
            current_state, next_state, a, char_encode_mod
        )
        current_state, next_state = next_state, current_state

    return current_state


@njit
def find_neighbors_assignment5_optimized(
    point_in: np.ndarray, point_out: np.ndarray, a: int, mod: int
) -> None:
    """Optimized neighbor finding without table lookup"""
    n = len(point_in)

    # Calculate first element
    y1 = (point_in[0] + a) % mod
    point_out[0] = y1
    x1 = point_in[0]

    # Unroll the loop pattern and optimize calculations
    i = 1
    while i < n:
        # Odd index: y_i = x_i - (x1 * y_{i-1})
        temp = point_in[i] - x1 * point_out[i - 1]
        point_out[i] = temp % mod

        i += 1
        if i < n:
            # Even index: y_i = x_i - (y1 * x_{i-1})
            temp = point_in[i] - y1 * point_in[i - 1]
            point_out[i] = temp % mod
            i += 1


@njit
def decode_assignment5_optimized(chars: np.ndarray, char_encode_mod: int, d_mod: int):
    """Optimized decode version"""
    current_state = chars.copy()
    next_state = np.empty_like(current_state)

    for a in range(d_mod - 1, -1, -1):
        reverse_find_neighbors_assignment5_optimized(
            current_state, next_state, a, char_encode_mod
        )
        current_state, next_state = next_state, current_state

    return current_state


@njit
def reverse_find_neighbors_assignment5_optimized(
    point_in: np.ndarray, point_out: np.ndarray, a: int, mod: int
) -> None:
    """Optimized reverse neighbor finding"""
    n = len(point_in)

    # Calculate first element
    x1 = (point_in[0] - a) % mod
    point_out[0] = x1
    y1 = point_in[0]

    # Unroll and optimize the reverse calculation
    i = 1
    while i < n:
        # Odd index: x_i = y_i + x1 * y_{i-1}
        temp = point_in[i] + x1 * point_in[i - 1]
        point_out[i] = temp % mod

        i += 1
        if i < n:
            # Even index: x_i = y_i + y1 * x_{i-1}
            temp = point_in[i] + y1 * point_out[i - 1]
            point_out[i] = temp % mod
            i += 1


# Alternative: In-place operations to reduce memory allocation


@njit
def encode_assignment5_inplace(chars: np.ndarray, char_encode_mod: int, d_mod: int):
    """In-place version to reduce memory allocations"""
    n = len(chars)
    temp_array = np.empty(n, dtype=chars.dtype)

    for a in range(d_mod):
        # Calculate transformations in temporary array
        y1 = (chars[0] + a) % char_encode_mod
        temp_array[0] = y1
        x1 = chars[0]

        for i in range(1, n):
            if i % 2 == 0:
                temp_array[i] = (chars[i] - y1 * chars[i - 1]) % char_encode_mod
            else:
                temp_array[i] = (chars[i] - x1 * temp_array[i - 1]) % char_encode_mod

        # Copy back to original array
        chars[:] = temp_array[:]

    return chars


# For very large arrays, consider chunked processing


@njit
def encode_assignment5_chunked(
    chars: np.ndarray, char_encode_mod: int, d_mod: int, chunk_size: int = 1000
):
    """Process in chunks for better cache locality with large arrays"""
    if len(chars) <= chunk_size:
        return encode_assignment5_optimized(chars, char_encode_mod, d_mod)

    # For large arrays, process the entire array at once is usually better
    # This is a placeholder for chunk-based processing if needed
    return encode_assignment5_optimized(chars, char_encode_mod, d_mod)


# Performance testing function


def benchmark_implementations():
    """Compare different implementations"""
    np.random.seed(42)
    n = 5659400
    chars = np.random.randint(0, 256, n, dtype=np.int32)
    char_encode_mod = 256
    d_mod = 100

    import time

    # Test optimized version
    start = time.perf_counter()
    result1 = encode_assignment5_optimized(chars.copy(), char_encode_mod, d_mod)
    time1 = time.perf_counter() - start

    # Test in-place version
    start = time.perf_counter()
    chars_copy = chars.copy()
    result2 = encode_assignment5_inplace(chars_copy, char_encode_mod, d_mod)
    time2 = time.perf_counter() - start

    print(f"Optimized version: {time1:.4f} seconds")
    print(f"In-place version: {time2:.4f} seconds")
    print(f"Results match: {np.array_equal(result1, result2)}")


# Additional optimization: Precompute modular arithmetic operations


@njit
def encode_assignment5_precomputed_mod(
    chars: np.ndarray, char_encode_mod: int, d_mod: int
):
    """Version with precomputed modular operations"""
    current_state = chars.copy()
    next_state = np.empty_like(current_state)

    # Precompute some values that don't change
    mod_mask = (
        char_encode_mod - 1 if (char_encode_mod & (char_encode_mod - 1)) == 0 else None
    )

    for a in range(d_mod):
        if mod_mask is not None:
            # Use bitwise AND for power-of-2 modulus (faster)
            find_neighbors_assignment5_bitwise(current_state, next_state, a, mod_mask)
        else:
            find_neighbors_assignment5_optimized(
                current_state, next_state, a, char_encode_mod
            )
        current_state, next_state = next_state, current_state

    return current_state


@njit
def find_neighbors_assignment5_bitwise(
    point_in: np.ndarray, point_out: np.ndarray, a: int, mod_mask: int
) -> None:
    """Use bitwise operations when modulus is power of 2"""
    n = len(point_in)

    y1 = (point_in[0] + a) & mod_mask
    point_out[0] = y1
    x1 = point_in[0]

    i = 1
    while i < n:
        # Odd index
        temp = point_in[i] - x1 * point_out[i - 1]
        point_out[i] = temp & mod_mask

        i += 1
        if i < n:
            # Even index
            temp = point_in[i] - y1 * point_in[i - 1]
            point_out[i] = temp & mod_mask
            i += 1


if __name__ == "__main__":
    benchmark_implementations()
