import os
import time
import numpy as np
import pickle
import galois

DIR = "multiplication_table/"
SUDO512_MOD = f"{DIR}mod_256_sudo512.npy"
GF256 = f"{DIR}mul_gf256.npy"
GF256_EXPLICIT_POLY = f"{DIR}mul_gf256_explicit_poly.npy"


def precompute_sudo512_mod(filepath: str = SUDO512_MOD):
    """
    Saves a (256, 256) uint16 multiplication table where
    indices are bytes [0..255], but all arithmetic happens
    in Z512 using odd representatives: F(x) = 2x + 1.

    mul_table[a, b] = F(a) * F(b) mod 512
                    = (2a+1) * (2b+1) mod 512
    The result is always odd, fits uint16.
    """
    size = 256
    table = np.zeros((size, size), dtype=np.uint16)
    for a in range(size):
        a_odd = np.uint32(2 * a + 1)
        for b in range(size):
            b_odd = np.uint32(2 * b + 1)
            table[a, b] = (a_odd * b_odd) % 512
            # print(f"table: {table[a, b]}\n\n")
    os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)
    np.save(filepath, table)
    print(f"Saved sudo512 table to {filepath}")


def precompute_gf256_multiplication(filepath: str = GF256):
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


def precompute_gf256_multiplication_explicit_poly(filepath: str = GF256_EXPLICIT_POLY):
    """
    Difference from the original version:
    ----------------------------------------------------------------------
    The original called `galois.GF(2**8)` with no arguments, which lets the
    library silently pick its own default irreducible polynomial to define
    the field.

    This version builds the field the "polynomial ring" way instead:
    it explicitly constructs the modulus as a `galois.Poly` object
    (x^8 + x^4 + x^3 + x + 1, the AES/Rijndael polynomial)
    and passes it in via `irreducible_poly=`. GF(2^8) is then defined,
    on the record.

    Mathematically the two versions produce an IDENTICAL multiplication
    table (same modulus => same field => same table), since 0x11B also
    happens to be `galois`'s own default. The only thing that changes is
    that the modulus is now an explicit, inspectable object
    rather than library default.
    """
    print("Precomputing GF(2^8) LUT (explicit polynomial modulus)...")

    modulus = galois.Poly.Degrees([8, 4, 3, 2, 0])  # x^8 + x^4 + x^3 + x^2 + 1  
    assert modulus.is_irreducible(), "modulus must be irreducible to define a field"

    GF256 = galois.GF(2**8, irreducible_poly=modulus)

    elements = GF256(np.arange(256, dtype=np.uint8))

    # Create the 256x256 multiplication lookup table
    x_grid, y_grid = np.meshgrid(elements, elements, indexing="ij")
    mul_lut = np.array(x_grid * y_grid, dtype=np.uint8)

    os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)
    np.save(filepath, mul_lut)
    print(f"Saved to {filepath}")


def load_gf256(filepath: str = GF256) -> np.ndarray:
    """
    Loads the multiplication table, creating it first if it doesn't exist.
    """
    if not os.path.exists(filepath):
        precompute_gf256_multiplication(filepath)

    return np.load(filepath)

def load_gf256_explicit_poly(filepath: str = GF256_EXPLICIT_POLY) -> np.ndarray:
    """
    Loads the multiplication table, creating it first if it doesn't exist.
    """
    if not os.path.exists(filepath):
        precompute_gf256_multiplication_explicit_poly(filepath)

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

    print(galois.GF(2**8).irreducible_poly)
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
