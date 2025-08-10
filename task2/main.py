import os
import sys
from helpers import (
    file_to_base64_txt,
    base64_txt_to_file,
    get_unique_filename,
    get_decoded_text,
    get_encoded_text,
)


def main():
    # Setup encoding parameters

    # NOTE: lib base64 can'n handle char_ecncode_mod > 128 (ValueError: string argument should contain only ASCII characters)
    # char_ecncode_mod = 256
    char_ecncode_mod = 128
    d_mod = 128
    # Handle input file
    if len(sys.argv) > 1:
        base_file = sys.argv[1]
    else:
        base_file = input("Enter file to encode (e.g., img.jpg): ").strip()

    if not os.path.exists(base_file):
        print(f"File '{base_file}' does not exist.")
        return

    # Handle base64 file encode/decode
    base_name, ext = os.path.splitext(base_file)
    ext = ext[1:]  # remove dot

    save_txt_path = get_unique_filename(base_name, "b64txt", "txt")
    encoded_img_path = get_unique_filename(base_name, "encoded", ext)
    decoded_img_path = get_unique_filename(base_name, "decoded", ext)

    file_to_base64_txt(base_file, save_txt_path)

    with open(save_txt_path, "r") as f:
        txt_file = f.read()

    print("Encoded base64 length:", len(txt_file))

    encoded_vector = get_encoded_text(txt_file, char_ecncode_mod, d_mod)
    decoded_vector = get_decoded_text(encoded_vector, char_ecncode_mod, d_mod)
    # Save encoded and decoded image files
    base64_txt_to_file(encoded_vector, encoded_img_path)
    base64_txt_to_file(decoded_vector, decoded_img_path)

    print(
        f"Saved:\n - Encoded file: {encoded_img_path}\n - Decoded file: {
            decoded_img_path
        }"
    )


if __name__ == "__main__":
    main()
