import base64
import numpy as np


def main():
    file_path = "test_files/bob.txt"

    with open(file_path, "rb") as file:
        np_arr = np.frombuffer(file.read(), dtype=np.uint8)

    print(np_arr)


if __name__ == "__main__":
    main()
