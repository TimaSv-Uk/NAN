import os
import time
import numpy as np
import pickle
import galois

DIR = "multiplication_table"


def precompute_256_sudo512(filepath: str = "multiplication_table/mod_256_sudo512.npy"):
    """
    Creates a multiplication table where elements are transformed
    via the 'Odd/No Pair' mapping from the 512 space.
    """
    print("Precomputing Sudo512 GF(2^8) LUT...")

    # Define your 'Half Elements' mapping
    # This takes the odd numbers from 0-511 and maps them to 0-255
    # Result: [1, 3, 5, ..., 255, 1, 3, 5, ..., 255]
    # We take the first 256 unique entries or a specific slice
    mapping = np.array([x % 256 for x in range(512) if x % 2 != 0], dtype=np.uint8)
    # Initialize Galois Field
    GF256 = galois.GF(2**8)
    # Apply the transformation to the elements before multiplication
    # Instead of [0, 1, 2...], we use your [1, 3, 5...]
    elements = GF256(mapping)
    x_grid, y_grid = np.meshgrid(elements, elements, indexing="ij")
    # Perform GF multiplication on 'odd' elements from mod512
    mul_lut = np.array(x_grid * y_grid, dtype=np.uint8)
    print(mul_lut)
    os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)
    np.save(filepath, mul_lut)
    print(f"Saved sudo512 table to {filepath}")


def precompute_gf256_multiplication(filepath: str = "mul_gf256.npy"):
    """
    Generates the GF(2^8) multiplication table and saves it as a .npy file.
    """
    print("Precomputing GF(2^8) LUT...")
    GF256 = galois.GF(2**8)

    elements = GF256(np.arange(256, dtype=np.uint8))

    # Create the 256x256 multiplication lookup table
    x_grid, y_grid = np.meshgrid(elements, elements, indexing="ij")
    mul_lut = np.array(x_grid * y_grid, dtype=np.uint8)

    # Ensure the directory exists if you are using a path like "multiplication_table/..."
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    np.save(filepath, mul_lut)
    print(f"Saved to {filepath}")


def load_gf256(filepath: str = "mul_gf256.npy") -> np.ndarray:
    """
    Loads the multiplication table, creating it first if it doesn't exist.
    """
    if not os.path.exists(filepath):
        precompute_gf256_multiplication(filepath)

    return np.load(filepath)


def precompute_multiplication(mod: int):
    arr = np.zeros((mod, mod), dtype=int)
    for i in range(mod):
        for j in range(mod):
            arr[i][j] = i * j
    np.save(f"multiplication_table/mul_mod_{mod}.npy", arr)


def precompute_multiplication_set(mod: int):
    set = {}
    for i in range(mod):
        for j in range(mod):
            set[(i, j)] = i * j
    with open(f"multiplication_table/mul_mod_{mod}.pkl", "wb") as file:
        pickle.dump(set, file)


def ensure_mul_table_exist(mod: int) -> str:
    """Create (if missing) and return path to a mod x mod table of (i*j) % mod."""
    os.makedirs(DIR, exist_ok=True)
    path = os.path.join(DIR, f"mul_mod_{mod}.npy")
    if not os.path.exists(path):
        precompute_multiplication(mod)
    return path


def read_precompute_multiplication(x: int, y: int, mod: int) -> int:
    path = f"multiplication_table/mul_mod_{mod}.npy"
    mmap_arr = np.load(path, mmap_mode="r")
    # print(x - from_val, y - from_val)
    return mmap_arr[x, y]


def read_precompute_multiplication_set(x: int, y: int, mod: int) -> int:
    path = f"multiplication_table/mul_mod_{mod}.pkl"
    with open(path, "rb") as file:
        arr = pickle.load(file)
    return arr[(x, y)]


if __name__ == "__main__":
    precompute_256_sudo512

    mod = 256

    precompute_multiplication(mod)
    precompute_multiplication_set(mod)
    # NOTE: Pickle (.pkl) read is ~10x faster than NumPy .npy
    start_time = time.perf_counter()
    end_time = time.perf_counter()
    print(read_precompute_multiplication(3, 2, mod))
    execution_time = end_time - start_time
    print(f"NP.ARRAY npy read_precompute_multiplication: {execution_time}")

    start_time = time.perf_counter()
    end_time = time.perf_counter()
    print(read_precompute_multiplication_set(3, 2, mod))
    execution_time = end_time - start_time
    print(f"SET pkl read_precompute_multiplication_set: {execution_time}")

    precompute_gf256_multiplication()
    # start_time = time.perf_counter()
    # end_time = time.perf_counter()
    # print(read_precompute_multiplication(257, 257, mod))
    # execution_time = end_time - start_time
    # print(f"read_precompute_multiplication: {execution_time}")
    #
    # start_time = time.perf_counter()
    # end_time = time.perf_counter()
    # print((257 * 257) % mod)
    # execution_time = end_time - start_time
    # print(f"multiplication: {execution_time}")
