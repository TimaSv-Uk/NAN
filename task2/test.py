import unittest
from task2 import (
    get_change_first_symbol_based_on_full_vector,
    reverse_change_first_symbol_based_on_full_vector,
    encode,
    decode,
    text_from_int_to_ascii,
)


class TestMathUtils(unittest.TestCase):
    def test_assignment2(self):
        with open("data2.txt", "r") as f:
            chars = f.read()
        # Setup encoding parameters
        char_ecncode_mod = 256
        d_mod = 128

        chars_int = [ord(char) % char_ecncode_mod for char in chars]
        # Handle input file
        chars_int_encoded = encode(chars_int, char_ecncode_mod, d_mod)
        encoded_text = text_from_int_to_ascii(chars_int_encoded)

        encoded_int_from_text = [ord(c) % char_ecncode_mod for c in encoded_text]
        decoded_text_int = decode(encoded_int_from_text, char_ecncode_mod, d_mod)
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
            "🔥🚀vsdvd",
        ]
        for text in test_cases:
            with self.subTest(text=text):
                chars = [ord(t) % char_ecncode_mod for t in text]
                new_vector = get_change_first_symbol_based_on_full_vector(
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
        with open("data2.txt", "r") as f:
            chars = f.read()

        char_ecncode_mod = 256
        d_mod = 128

        # Step 1: convert text to int list
        chars_int = [ord(char) % char_ecncode_mod for char in chars]
        # Step 2: apply change to first symbol
        encoded_with_first = get_change_first_symbol_based_on_full_vector(
            chars_int, char_ecncode_mod
        )

        # Step 3: encode full list
        encoded = encode(encoded_with_first, char_ecncode_mod, d_mod)

        # Step 4: convert to text
        encoded_text = text_from_int_to_ascii(encoded)

        # Step 5: decode text to int
        encoded_int_from_text = [ord(c) % char_ecncode_mod for c in encoded_text]

        # Step 6: decode
        decoded = decode(encoded_int_from_text, char_ecncode_mod, d_mod)

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

    def test_assignment3_3(self):
        text1 = "3456701289"
        text2 = "3456701280"

        char_ecncode_mod = 256
        d_mod = 128

        encoded_text1 = get_encoded_text(text1, char_ecncode_mod, d_mod)
        encoded_text2 = get_encoded_text(text2, char_ecncode_mod, d_mod)

        print("In text1:", text1)
        print("Encoded text1:", encoded_text1)

        print("In text2:", text2)
        print("Encoded text2:", encoded_text2)

        self.assertNotEqual(encoded_text1, encoded_text2)


def get_encoded_text(text, char_ecncode_mod, d_mod):
    chars_int = [ord(char) % char_ecncode_mod for char in text]
    encoded_with_first = get_change_first_symbol_based_on_full_vector(
        chars_int, char_ecncode_mod
    )
    encoded = encode(encoded_with_first, char_ecncode_mod, d_mod)
    encoded_text = text_from_int_to_ascii(encoded)
    return encoded_text


if __name__ == "__main__":
    unittest.main()
    # tests = TestMathUtils()
    # # tests.test_assignment3()
    # # tests.test_assignment3_2()
    # tests.test_assignment2()
