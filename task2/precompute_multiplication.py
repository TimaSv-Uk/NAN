import os
import time
import numpy as np

DIR = "multiplication_table"


def precompute_multiplication(mod: int):
    arr = np.zeros((mod, mod), dtype=int)
    for i in range(mod):
        for j in range(mod):
            arr[i][j] = i * j
    print(arr)
    np.save(f"multiplication_table/mul_mod_{mod}.npy", arr)


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


if __name__ == "__main__":
    mod = 258
    precompute_multiplication(mod)

    print(read_precompute_multiplication(3, 2, mod))
    print(read_precompute_multiplication(3, 2, mod))

    start_time = time.perf_counter()
    end_time = time.perf_counter()
    print(read_precompute_multiplication(257, 257, mod))
    execution_time = end_time - start_time
    print(f"read_precompute_multiplication: {execution_time}")

    start_time = time.perf_counter()
    end_time = time.perf_counter()
    print((257 * 257) % mod)
    execution_time = end_time - start_time
    print(f"multiplication: {execution_time}")
