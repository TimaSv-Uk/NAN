import unittest
from helpers import (
    text_sameness_percentage,
    bites_sameness_percentage,
    get_encoded_text,
    get_decoded_text,
    load_file_to_bites,
)
from task2 import (
    encode_assignment5,
    change_first_symbol_based_on_random_vector,
    change_first_symbol_based_on_full_vector,
)

import numpy as np
import random


class TestMathUtils(unittest.TestCase):
    def test_decode_encode_functions(self):
        with open("test_files/data2.txt", "r") as f:
            chars = f.read()

        char_ecncode_mod = 256
        d_mod = 128
        encoded = get_encoded_text(chars, char_ecncode_mod, d_mod)
        decoded = get_decoded_text(encoded, char_ecncode_mod, d_mod)

        # print("Encoded text:", encoded)
        # print("Decoded text:", decoded)
        self.assertEqual(chars, decoded)

    def test_text_sameness_encoding_resultsassignment5(self):
        char_ecncode_mod = 256
        d_mod = 128

        with open("test_files/data2.txt", "r") as f:
            data2 = f.read()

        with open("test_files/data2_changed.txt", "r") as f:
            data2_changed = f.read()
        test_cases = [
            ("3456701289", "3456701280"),
            ("abc123", "abc124"),
            ("vsdvd", "vsdve"),
            ("same text", "same text"),  # to test sameness
            ("short", "longer text"),
            (data2, data2_changed),
        ]
        with open(
            "test_text_sameness_encoding_results_assignment5.txt", "w", encoding="utf-8"
        ) as f:
            for text1, text2 in test_cases:
                with self.subTest(text1=text1, text2=text2):
                    encoded_text1 = get_encoded_text(text1, char_ecncode_mod, d_mod)
                    encoded_text2 = get_encoded_text(text2, char_ecncode_mod, d_mod)
                    percent = text_sameness_percentage(encoded_text1, encoded_text2)

                    f.write(f"Text 1: {text1}\n")
                    f.write(f"Text 2: {text2}\n")
                    f.write(f"Encoded Text 1: {encoded_text1}\n")
                    f.write(f"Encoded Text 2: {encoded_text2}\n")
                    f.write(f"Sameness %: {percent}%\n")
                    f.write("-" * 50 + "\n")
                    if text1 == text2:
                        self.assertEqual(encoded_text1, encoded_text2)
                    else:
                        self.assertNotEqual(encoded_text1, encoded_text2)

    def test_text_sameness_encoding_results(self):
        char_ecncode_mod = 256
        d_mod = 128

        with open("test_files/data2.txt", "r") as f:
            data2 = f.read()

        with open("test_files/data2_changed.txt", "r") as f:
            data2_changed = f.read()
        test_cases = [
            ("3456701289", "3456701280"),
            ("abc123", "abc124"),
            ("vsdvd", "vsdve"),
            ("same text", "same text"),  # to test sameness
            ("short", "longer text"),
            (data2, data2_changed),
        ]
        with open(
            "test_text_sameness_encoding_results.txt", "w", encoding="utf-8"
        ) as f:
            for text1, text2 in test_cases:
                with self.subTest(text1=text1, text2=text2):
                    encoded_text1 = get_encoded_text(text1, char_ecncode_mod, d_mod)
                    encoded_text2 = get_encoded_text(text2, char_ecncode_mod, d_mod)
                    percent = text_sameness_percentage(encoded_text1, encoded_text2)

                    f.write(f"Text 1: {text1}\n")
                    f.write(f"Text 2: {text2}\n")
                    f.write(f"Encoded Text 1: {encoded_text1}\n")
                    f.write(f"Encoded Text 2: {encoded_text2}\n")
                    f.write(f"Sameness %: {percent}%\n")
                    f.write("-" * 50 + "\n")
                    if text1 == text2:
                        self.assertEqual(encoded_text1, encoded_text2)
                    else:
                        self.assertNotEqual(encoded_text1, encoded_text2)

    def test_text_sameness_FILE_encoding_results_change_first_symbol_based_on_random_vector(
        self,
    ):
        # file_path = "test_files/data2.txt"
        file_name = "img.jpg"
        # file_name = "vid_31mb.mp4"
        file_path = f"test_files/{file_name}"

        save_results_path = f"test_text_sameness_FILE_encoding_results_change_first_symbol_based_on_random_vector_{
            file_name.split('.')[0]
        }.txt"
        seed = 42

        file_bites = load_file_to_bites(file_path)  # np.array dtype=uint8

        file_bites_based_on_random_vector = change_first_symbol_based_on_random_vector(
            file_bites, seed
        )
        encoded_original = encode_assignment5(
            file_bites_based_on_random_vector, 256, 128
        )

        # Ensure deterministic encoding
        encoded_original_2 = encode_assignment5(
            file_bites_based_on_random_vector, 256, 128
        )
        self.assertTrue(np.array_equal(encoded_original, encoded_original_2))

        length = len(file_bites)
        quarter_indices = [length // 4, length // 2, 3 * length // 4, length - 1]

        with open(save_results_path, "w", encoding="utf-8") as f:
            for i, idx in enumerate(quarter_indices, 1):
                with self.subTest(quarter=i):
                    modified_bites = file_bites.copy()

                    # Pick a random new value different from original
                    original_val = int(modified_bites[idx])
                    new_val = random.randint(0, 255)
                    while new_val == original_val:
                        new_val = random.randint(0, 255)

                    modified_bites[idx] = np.uint8(new_val)

                    modified_bites = change_first_symbol_based_on_random_vector(
                        modified_bites, seed + 1
                    )

                    encoded_modified = encode_assignment5(modified_bites, 256, 128)

                    percent = bites_sameness_percentage(
                        encoded_original, encoded_modified
                    )

                    # Write to file
                    f.write(f"Quarter {i} change at index {idx}\n")
                    f.write(
                        f"Original byte: {original_val}, Modified byte: {new_val}\n"
                    )
                    f.write(f"Sameness %: {percent}%\n")
                    f.write("-" * 50 + "\n")

                    self.assertLess(percent, 100)

    def test_text_sameness_FILE_encoding_results_change_first_symbol_based_on_full_vector(
        self,
    ):
        file_name = "img.jpg"
        # file_path = "test_files/data2.txt"
        # file_name = "vid_31mb.mp4"

        file_path = f"test_files/{file_name}"

        save_results_path = f"test_text_sameness_FILE_encoding_results_change_first_symbol_based_on_full_vector_{
            file_name.split('.')[0]
        }.txt"

        file_bites = load_file_to_bites(file_path)  # np.array dtype=uint8

        file_bites_based_on_random_vector = change_first_symbol_based_on_full_vector(
            file_bites
        )
        encoded_original = encode_assignment5(
            file_bites_based_on_random_vector, 256, 128
        )

        # Ensure deterministic encoding
        encoded_original_2 = encode_assignment5(
            file_bites_based_on_random_vector, 256, 128
        )
        self.assertTrue(np.array_equal(encoded_original, encoded_original_2))

        length = len(file_bites)
        quarter_indices = [length // 4, length // 2, 3 * length // 4, length - 1]

        with open(save_results_path, "w", encoding="utf-8") as f:
            for i, idx in enumerate(quarter_indices, 1):
                with self.subTest(quarter=i):
                    modified_bites = file_bites.copy()

                    # Pick a random new value different from original
                    original_val = int(modified_bites[idx])
                    new_val = random.randint(0, 255)
                    while new_val == original_val:
                        new_val = random.randint(0, 255)

                    modified_bites[idx] = np.uint8(new_val)

                    modified_bites = change_first_symbol_based_on_full_vector(
                        modified_bites
                    )

                    encoded_modified = encode_assignment5(modified_bites, 256, 128)

                    percent = bites_sameness_percentage(
                        encoded_original, encoded_modified
                    )

                    # Write to file
                    f.write(f"Quarter {i} change at index {idx}\n")
                    f.write(
                        f"Original byte: {original_val}, Modified byte: {new_val}\n"
                    )
                    f.write(f"Sameness %: {percent}%\n")
                    f.write("-" * 50 + "\n")

                    self.assertLess(percent, 100)


if __name__ == "__main__":
    unittest.main()
