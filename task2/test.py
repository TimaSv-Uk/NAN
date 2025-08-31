import unittest
from assignment2 import (
    encode_assignment2,
    decode_assignment2,
)
from task2 import (
    change_first_symbol_based_on_full_vector,
    reverse_change_first_symbol_based_on_full_vector,
    encode_assignment5,
    decode_assignment5,
)
from helpers import (
    text_from_int_to_ascii,
    text_sameness_percentage,
    get_encoded_text,
    get_decoded_text,
)


class TestMathUtils(unittest.TestCase):
    def test_assignment2(self):
        with open("test_files/data2.txt", "r") as f:
            chars = f.read()
        # Setup encoding parameters
        char_ecncode_mod = 256
        d_mod = 128

        chars_int = [ord(char) % char_ecncode_mod for char in chars]
        # Handle input file
        chars_int_encoded = encode_assignment2(chars_int, char_ecncode_mod, d_mod)
        encoded_text = text_from_int_to_ascii(chars_int_encoded)

        encoded_int_from_text = [ord(c) % char_ecncode_mod for c in encoded_text]
        decoded_text_int = decode_assignment2(
            encoded_int_from_text, char_ecncode_mod, d_mod
        )
        decoded_text = text_from_int_to_ascii(decoded_text_int)

        # print("Encoded text:", encoded_text)
        # print("Decoded text:", decoded_text)
        self.assertEqual(chars, decoded_text)

    def test_assignment3(self):
        char_ecncode_mod = 256
        test_cases = [
            "hello world",
            "test123",
            "abcXYZ",
            "abcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZabcXYZ",
            "a",
            "vsdvd",
        ]
        for text in test_cases:
            with self.subTest(text=text):
                chars = [ord(t) % char_ecncode_mod for t in text]
                new_vector = change_first_symbol_based_on_full_vector(
                    chars, char_ecncode_mod
                )

                initial_vector = reverse_change_first_symbol_based_on_full_vector(
                    new_vector, char_ecncode_mod
                )
                # print(
                #     f"First node\n in text: {chars[0]},encoded text: {
                #         new_vector[0]
                #     },decoded text: {initial_vector[0]}"
                # )
                self.assertEqual(chars, initial_vector)

    def test_assignment3_2(self):
        with open("test_files/data2.txt", "r") as f:
            chars = f.read()

        char_ecncode_mod = 256
        d_mod = 128

        # Step 1: convert text to int list
        chars_int = [ord(char) % char_ecncode_mod for char in chars]
        # Step 2: apply change to first symbol
        encoded_with_first = change_first_symbol_based_on_full_vector(
            chars_int, char_ecncode_mod
        )

        # Step 3: encode full list
        encoded = encode_assignment2(encoded_with_first, char_ecncode_mod, d_mod)

        # Step 4: convert to text
        encoded_text = text_from_int_to_ascii(encoded)

        # Step 5: decode text to int
        encoded_int_from_text = [ord(c) % char_ecncode_mod for c in encoded_text]

        # Step 6: decode
        decoded = decode_assignment2(encoded_int_from_text, char_ecncode_mod, d_mod)

        # Step 7: reverse change of first symbol (M⁻¹)
        reversed_first_symbol = reverse_change_first_symbol_based_on_full_vector(
            decoded, char_ecncode_mod
        )

        # Step 8: convert back to string
        decoded_text = text_from_int_to_ascii(reversed_first_symbol)

        # print("In text:", chars)
        # print("Encoded text:", encoded_text)
        # print("Decoded text:", decoded_text)

        self.assertEqual(chars, decoded_text)

    def test_decode_encode_functions(self):
        with open("test_files/data2.txt", "r") as f:
            chars = f.read()

        char_ecncode_mod = 256
        d_mod = 128
        encoded = get_encoded_text(chars, char_ecncode_mod, d_mod, encode_assignment2)
        decoded = get_decoded_text(encoded, char_ecncode_mod, d_mod, decode_assignment2)

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
                    encoded_text1 = get_encoded_text(
                        text1, char_ecncode_mod, d_mod, encode_assignment2
                    )
                    encoded_text2 = get_encoded_text(
                        text2, char_ecncode_mod, d_mod, encode_assignment2
                    )
                    percent = text_sameness_percentage(encoded_text1, encoded_text2)

                    # print(f"\n\n")
                    # print(f"In text1: {text1}")
                    # print(f"Encoded text1: {encoded_text1}")
                    # print(f"In text2: {text2}")
                    # print(f"Encoded text2: {encoded_text2}")
                    # print("text_sameness_percentage: ", percent)

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

    def test_assignment5_not_same_as_original_algorithm(self):
        with open("test_files/data2.txt", "r") as f:
            text = f.read()
        char_ecncode_mod = 256
        d_mod = 128

        original_algorithm = get_encoded_text(
            text, char_ecncode_mod, d_mod, encode_assignment2
        )
        assignment5_algorithm = get_encoded_text(
            text, char_ecncode_mod, d_mod, encode_assignment5
        )
        self.assertNotEqual(original_algorithm, assignment5_algorithm)

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
                    encoded_text1 = get_encoded_text(
                        text1, char_ecncode_mod, d_mod, encode_assignment5
                    )
                    encoded_text2 = get_encoded_text(
                        text2, char_ecncode_mod, d_mod, encode_assignment5
                    )
                    percent = text_sameness_percentage(encoded_text1, encoded_text2)

                    # print(f"\n\n")
                    # print(f"In text1: {text1}")
                    # print(f"Encoded text1: {encoded_text1}")
                    # print(f"In text2: {text2}")
                    # print(f"Encoded text2: {encoded_text2}")
                    # print("text_sameness_percentage: ", percent)

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
    # tests = TestMathUtils()
    # # tests.test_assignment3()
    # # tests.test_assignment3_2()
    # tests.test_assignment2()
