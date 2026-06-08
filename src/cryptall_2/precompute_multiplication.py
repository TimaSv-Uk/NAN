import os
import time
import numpy as np
import pickle
import galois

DIR = "multiplication_table/"
SUDO512_MOD = f"{DIR}mod_256_sudo512.npy"


def precompute_sudo512_mod(filepath: str = SUDO512_MOD):
    """
    Creates a multiplication table where elements are transformed
    via the 'Odd/No Pair' mapping from the 512 space.


    Reverse Mapping (Modulo 512 to Byte):When decoding, you take your odd number
    y and map it back to the original byte **x = (y - 1) / 2**

    Forward Mapping (Byte to Modulo 512): You take your 8-bit input
    x (where x in [0, 255]) and map it to an odd number **y = (2x + 1)mod{512}**
    NOTE: if array is not converted to larger int type you wont exact mapping up to 511

    """

    mapping = np.array([x for x in range(512) if x % 2 != 0], dtype=np.uint16)
    # EXAMPLE: Forward Mapping
    # mapping = np.array([(x - 1) / 2 for x in range(512) if x % 2 != 0], dtype=np.uint8)
    # EXAMPLE: Forward Mapping
    # ran = [(x * 2 + 1) for x in mapping]
    # print(ran)
    os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)
    np.save(filepath, mapping)
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


def load_sudo512_mod(filepath: str = SUDO512_MOD) -> np.ndarray:
    """
    Loads the multiplication table, creating it first if it doesn't exist.
    """
    if not os.path.exists(filepath):
        precompute_sudo512_mod(filepath)

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
    precompute_sudo512_mod()

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
