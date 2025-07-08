import base64
import os
import sys


def write_text_to_file(file_name, text):
    f = open(file_name, "w")
    f.write(text)

    f.close()


def text_from_int_to_ascii(point):
    #  read file

    decoded_text = [chr(int(element)) for element in point]
    return "".join(decoded_text)


def find_neigbors_N_a(point, a, mod):
    # N_a(X) = [x1+a, z2, z3, ..., zn]
    # де:
    # z2 = x1 * (x1 + a) - x2
    # z3 = x1 * z2 - x3
    # ...
    # zn = x1 * z(n-1) - xn
    point = point.copy()
    neigbor_point = []

    for i, coord in enumerate(point):
        if i == 0:
            x1 = (point[0] + a) % mod
            neigbor_point.append(x1)
        elif i == 1:
            z2 = (point[0] * (point[0] + a) - point[i]) % mod
            neigbor_point.append(z2)
        else:
            z_i = (point[0] * neigbor_point[-1] - point[i]) % mod
            neigbor_point.append(z_i)
    return neigbor_point


def find_neigbors_M_a(point, a, mod):
    # M_a(X) = [y1+a, z2, z3, ..., zn]
    # де:
    # z2 = y1 * (y1 + a) - x2
    # z3 = (y1 + a) * z2 - x3
    point = point.copy()
    neigbor_point = []

    for i, coord in enumerate(point):
        if i == 0:
            y1 = (point[0] + a) % mod
            neigbor_point.append(y1)
        elif i == 1:
            z2 = (point[0] * (point[0] + a) - point[i]) % mod
            neigbor_point.append(z2)
        else:
            z_i = ((point[0] + a) * neigbor_point[-1] - point[i]) % mod
            neigbor_point.append(z_i)
    return neigbor_point


# NOTE: decode
# n від - as
# n - a1
# M as-1
# last step N - a1
def reverce_find_neigbors_N_a(point, a, mod):
    # Reverse of N_a(X) = [x1+a, z2, z3, ..., zn]
    # where:
    # z2 = x1 * (x1 + a) - x2  =>  x2 = x1 * (x1 + a) - z2
    # z3 = x1 * z2 - x3  =>  x3 = x1 * z2 - z3
    # ...
    # zn = x1 * z(n-1) - xn  =>  xn = x1 * z(n-1) - zn
    point = point.copy()
    original_point = []

    for i in range(len(point)):
        if i == 0:
            x1 = (point[0] - a) % mod
            original_point.append(x1)
        elif i == 1:
            x2 = (original_point[0] * (original_point[0] + a) - point[i]) % mod
            original_point.append(x2)
        else:
            xi = (original_point[0] * point[i - 1] - point[i]) % mod
            original_point.append(xi)
    return original_point


def reverce_find_neigbors_M_a(point, a, mod):
    # Reverse of M_a(X) = [y1+a, z2, z3, ..., zn]
    # where:
    # z2 = y1 * (y1 + a) - x2  =>  x2 = y1 * (y1 + a) - z2
    # z3 = (y1 + a) * z2 - x3  =>  x3 = (y1 + a) * z2 - z3
    # ...
    # zn = (y1 + a) * z(n-1) - xn  =>  xn = (y1 + a) * z(n-1) - zn

    point = point.copy()
    original_point = []

    for i in range(len(point)):
        if i == 0:
            # x1 = z1 - a
            x1 = (point[0] - a) % mod
            original_point.append(x1)
        elif i == 1:
            # x2 = x1 * (x1 + a) - z2
            x2 = (original_point[0] * (original_point[0] + a) - point[i]) % mod
            original_point.append(x2)
        else:
            # xi = (x1 + a) * z(i-1) - zi
            xi = ((original_point[0] + a) * point[i - 1] - point[i]) % mod
            original_point.append(xi)
    return original_point


def encode(text: str, char_ecncode_mod: int, d_mod: int):
    chars = [ord(t) % char_ecncode_mod for t in text]

    d = [i for i in range(d_mod)]
    for a in d:
        if a % 2 == 0:
            chars = find_neigbors_N_a(chars, a, char_ecncode_mod)
            # print(chars, "Nx")
        else:
            chars = find_neigbors_M_a(chars, a, char_ecncode_mod)
            # print(chars, "My")
    return chars


def decode(encoded_text: str, char_ecncode_mod: int, d_mod: int):
    chars = [ord(t) % char_ecncode_mod for t in encoded_text]
    for a in reversed(range(d_mod)):
        if a % 2 == 0:
            chars = reverce_find_neigbors_N_a(chars, a, char_ecncode_mod)
            # print(f"After reverse N_a({a}): {chars}")
        else:
            chars = reverce_find_neigbors_M_a(chars, a, char_ecncode_mod)
            # print(f"After reverse M_a({a}): {chars}")
    return chars


def file_to_base64_txt(file_path, save_txt_path):
    with open(file_path, "rb") as file:
        encoded = base64.b64encode(file.read()).decode("utf-8")

    with open(save_txt_path, "w", encoding="utf-8") as txt_file:
        txt_file.write(encoded)
    print(f"{file_path} encoded to Base64 and saved to {save_txt_path}")


def base64_txt_to_file(text, output_file_path):
    decoded_data = base64.b64decode(text)

    with open(output_file_path, "wb") as output_file:
        output_file.write(decoded_data)
    print(f"decoded and saved to {output_file_path}")


def get_unique_filename(base_name, suffix, extension):
    i = 1
    while True:
        filename = f"{base_name}_{suffix}_{i}.{extension}"
        if not os.path.exists(filename):
            return filename
        i += 1


def main():
    # Setup encoding parameters
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

    # Encode/decode text part
    try:
        with open("data2.txt", "r") as f:
            chars = f.read()
        print("Start text:", chars)

        chars = encode(chars, char_ecncode_mod, d_mod)
        encoded_text = text_from_int_to_ascii(chars)
        decoded_text_int = decode(encoded_text, char_ecncode_mod, d_mod)
        decoded_text = text_from_int_to_ascii(decoded_text_int)

        print("Encoded text:", encoded_text)
        print("Decoded text:", decoded_text)

        write_text_to_file("solution_task2.txt", encoded_text)
        write_text_to_file("solution_task2_decoded.txt", decoded_text)
    except Exception as e:
        print(f"Warning: Could not encode text part: {e}")

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

    encoded_vector = encode(txt_file, char_ecncode_mod, d_mod)
    decoded_vector = decode(
        text_from_int_to_ascii(encoded_vector), char_ecncode_mod, d_mod
    )

    # Save encoded and decoded image files
    base64_txt_to_file(text_from_int_to_ascii(encoded_vector), encoded_img_path)
    base64_txt_to_file(text_from_int_to_ascii(decoded_vector), decoded_img_path)

    print(
        f"Saved:\n - Encoded file: {encoded_img_path}\n - Decoded file: {decoded_img_path}"
    )


main()
