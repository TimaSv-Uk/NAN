import unittest

from cryptall_2.encode_decode import (
    encode_bites,
    decode_bites,
    encode_bites_rand,
    encode_bites_full,
    remove_noise,
)

from cryptall_2.core import (
    encode_assignment10,
    decode_assignment10,
    encode_v5,
    decode_v5,
    modInverse,
)
from cryptall_2.helpers import (
    bites_sameness_percentage,
    load_file_to_bites,
    sudo_random_array,
)
from cryptall_2.core import randomize_d_mod

import numpy as np
import random
import time


class TestMathUtils(unittest.TestCase):
    """
    To run all test
    uv run pytest tests/tests.py

    To run selected test
    uv run pytest -s tests/tests.py::TestMathUtils::test_encode_decode_dmod1
    """

    def setUp(self):
        self.char_mod = 256
        self.d_mod = 128
        self.seed = 50

        self.random_d_mod_range = randomize_d_mod(self.d_mod, self.seed)
        self.test_file_dir = "./tests/test_files/"
        self.test_results_file_dir = "./tests/test_results/"
        self.file_names = {
            "txt": "data2.txt",
            "img": "img.jpg",
            "vid": "vid_27mb.mp4",
            "big_csv": "csv_100mb.csv",
        }

    def test_encode_decode_consistency(self):
        """Test that encoding followed by decoding restores the original bites."""
        file_bites = load_file_to_bites(f"{self.test_file_dir}{self.file_names['txt']}")
        encoded = encode_bites(file_bites, self.char_mod, self.d_mod, self.seed)
        decoded = decode_bites(encoded, self.char_mod, self.d_mod, self.seed)
        self.assertTrue(np.array_equal(file_bites, decoded))

    def test_encode_decode_dmod0(self):
        """Test that encoding followed by decoding restores the original bites."""
        file_bites = load_file_to_bites(f"{self.test_file_dir}{self.file_names['txt']}")

        print(file_bites)
        encoded = encode_bites(file_bites, self.char_mod, 0, self.seed)
        print(encoded)
        decoded = decode_bites(encoded, self.char_mod, 0, self.seed)

        print(decoded)
        self.assertTrue(np.array_equal(file_bites, decoded))

    def test_encode_decode_dmod1(self):
        """Test that encoding followed by decoding restores the original bites."""
        file_bites = load_file_to_bites(f"{self.test_file_dir}{self.file_names['txt']}")

        print(file_bites)
        encoded = encode_bites(file_bites, self.char_mod, 1, self.seed)
        print(encoded)
        decoded = decode_bites(encoded, self.char_mod, 1, self.seed)

        print(decoded)
        self.assertTrue(np.array_equal(file_bites, decoded))

    def test_randomized_d_mod_changes_order(self):
        """Check that randomize_d_mod changes the default sequence."""
        arr_range = np.arange(self.d_mod)
        randomized = randomize_d_mod(self.d_mod, self.seed)
        self.assertFalse(np.array_equal(arr_range, randomized))

    def _test_file_encoding_sameness(
        self, file_key: str, encode_func, seed: int, save_prefix: str
    ):
        """Helper to test file encoding sameness and save results to a file."""
        file_path = f"{self.test_file_dir}{self.file_names[file_key]}"
        save_path = f"{self.test_results_file_dir}{save_prefix}_{
            self.file_names[file_key].split('.')[0]
        }.txt"

        file_bites = load_file_to_bites(file_path)
        encoded_base = encode_func(file_bites, self.char_mod, self.d_mod, seed)

        # Deterministic check
        encoded_base2 = encode_func(file_bites, self.char_mod, self.d_mod, seed)
        self.assertTrue(np.array_equal(encoded_base, encoded_base2))

        length = len(file_bites)
        quarter_indices = [length // 4, length // 2, 3 * length // 4, length - 1]

        with open(save_path, "w", encoding="utf-8") as f:
            for i, idx in enumerate(quarter_indices, 1):
                with self.subTest(quarter=i):
                    modified_bites = file_bites.copy()

                    original_val = int(modified_bites[idx])
                    new_val = random.randint(0, 255)
                    while new_val == original_val:
                        new_val = random.randint(0, 255)
                    modified_bites[idx] = np.uint8(new_val)

                    encoded_modified = encode_func(
                        modified_bites,
                        self.char_mod,
                        self.d_mod,
                        seed + 1 if "rand" in encode_func.__name__ else seed,
                    )
                    percent = bites_sameness_percentage(encoded_base, encoded_modified)

                    # Save results to file
                    f.write(f"Quarter {i} change at index {idx}\n")
                    f.write(
                        f"Original byte: {original_val}, Modified byte: {new_val}\n"
                    )
                    f.write(f"Sameness %: {percent}%\n")
                    f.write("-" * 50 + "\n")

                    self.assertLess(percent, 100)

    def test_text_sameness_FILE_encoding(self):
        # file_lable = "vid"
        file_lable = "img"

        # test_text_sameness_FILE_encoding_rand
        self._test_file_encoding_sameness(
            file_lable, encode_bites_rand, self.seed, "results_rand"
        )

        # test_text_sameness_FILE_encoding_full
        self._test_file_encoding_sameness(
            file_lable, encode_bites_full, self.seed, "results_full"
        )
        # test_text_sameness_original_d_mod
        self._test_file_encoding_sameness(
            file_lable, encode_bites, self.seed, "results_original_d_mod"
        )

    def test_execution_time(self):
        for file_name in self.file_names.values():
            file_bites = load_file_to_bites(f"{self.test_file_dir}{file_name}")
            print(f"File name: {file_name}")
            print(f"Generated array of size: {file_bites.shape} bytes\n")

            start_time = time.perf_counter()
            encoded = encode_bites(file_bites, self.char_mod, self.d_mod, self.seed)
            end_time = time.perf_counter()
            execution_time = end_time - start_time
            print(f"Encoded_vector execution_time: {execution_time}")

            start_time = time.perf_counter()
            decoded = decode_bites(encoded, self.char_mod, self.d_mod, self.seed)
            end_time = time.perf_counter()
            execution_time = end_time - start_time
            print(f"Decoded_vector execution_time: {execution_time}\n")

    def test_isert_rand_array(self):
        random_array_length = 3
        random_array = sudo_random_array(random_array_length, 256, self.seed, np.uint8)
        original_arr = [1, 2, 4]
        new_arr = np.append(random_array, original_arr)

        self.assertEqual(len(new_arr) - 3, random_array_length)
        self.assertEqual(len(new_arr) - 3, random_array_length)
        self.assertTrue(np.array_equal(original_arr, new_arr[random_array_length:]))

    def test_digest_with_no_noise(self):
        file_path = f"{self.test_file_dir}{self.file_names['big_csv']}"
        file_bites = load_file_to_bites(file_path)
        number_of_digests = 10
        noise_ratio = 0.05

        encode_no_noise = encode_bites(file_bites, self.char_mod, self.d_mod, self.seed)

        encode_with_noise = encode_bites(
            file_bites, self.char_mod, self.d_mod, self.seed, noise_ratio
        )
        encode_with_noise = remove_noise(
            encode_with_noise, self.char_mod, self.seed, noise_ratio
        )
        self.assertFalse(np.array_equal(encode_no_noise, encode_with_noise))

        digests_no_noise = np.array_split(encode_no_noise, number_of_digests)
        digests_with_noise = np.array_split(encode_with_noise, number_of_digests)
        comparison_lines = []
        for i, (d1, d2) in enumerate(zip(digests_no_noise, digests_with_noise)):
            equal = np.array_equal(d1, d2)

            if equal:
                comparison_lines.append(f"Digest {i}: IDENTICAL\n")
            else:
                diff_count = bites_sameness_percentage(d1, d2)
                comparison_lines.append(
                    f"Digest {i}: DIFFERENT — {diff_count} bytes differ\n"
                )

        report_path = f"{self.test_file_dir}_digest_comparison_report.txt"

        with open(report_path, "w", encoding="utf-8") as f:
            f.writelines(comparison_lines)


if __name__ == "__main__":
    unittest.main()
