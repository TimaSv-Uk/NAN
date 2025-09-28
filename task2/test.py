import unittest
from helpers import (
    text_sameness_percentage,
    bites_sameness_percentage,
    load_file_to_bites,
    encode_bites,
    decode_bites,
    encode_bites_rand,
    decode_bites_rand,
    decode_bites_full,
    encode_bites_full,
)
from task2 import (
    randomize_d_mod,
)

import numpy as np
import random


class TestMathUtils(unittest.TestCase):
    def setUp(self):
        self.char_mod = 256
        self.d_mod = 128
        self.seed = 50

        self.random_d_mod_range = randomize_d_mod(self.d_mod, self.seed)
        self.test_file_dir = "test_files/"
        self.test_results_file_dir = "test_results/"
        self.file_names = {
            "txt": "data2.txt",
            "img": "img.jpg",
            "vid": "vid_31mb.mp4",
        }

    def test_encode_decode_consistency(self):
        """Test that encoding followed by decoding restores the original bites."""
        file_bites = load_file_to_bites(f"{self.test_file_dir}{self.file_names['txt']}")
        encoded = encode_bites(file_bites, self.char_mod, self.d_mod, self.seed)
        decoded = decode_bites(encoded, self.char_mod, self.d_mod, self.seed)
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
        file_path = f"test_files/{self.file_names[file_key]}"
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

    def test_text_sameness_FILE_encoding_rand(self):
        self._test_file_encoding_sameness(
            "vid", encode_bites_rand, self.seed, "results_rand"
        )

    def test_text_sameness_FILE_encoding_full(self):
        self._test_file_encoding_sameness(
            "vid", encode_bites_full, self.seed, "results_full"
        )

    def test_text_sameness_original_d_mod(self):
        self._test_file_encoding_sameness(
            "vid", encode_bites, self.seed, "results_original_d_mod"
        )


if __name__ == "__main__":
    unittest.main()
