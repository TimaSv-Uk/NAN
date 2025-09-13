import unittest
from helpers import (
    text_sameness_percentage,
    get_encoded_text,
    get_decoded_text,
)


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


if __name__ == "__main__":
    unittest.main()
