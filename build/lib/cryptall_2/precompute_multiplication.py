import os
import time
import numpy as np
import pickle

DIR = "multiplication_table"


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
