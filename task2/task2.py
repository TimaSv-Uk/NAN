def read_text_to_ascii(file_name, char_ecncode_mod):
    #  read file
    f = open(file_name, "r")

    text = f.read()

    chars = [ord(t) % char_ecncode_mod for t in text]
    f.close()
    return chars


def write_text_to_file(file_name, text):
    f = open(file_name, "w")
    f.write(text)

    f.close()


def text_from_int_to_ascii(point):
    #  read file

    decoded_text = [chr(int(element) % 256) for element in point]
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
    # z2 = y1 * (y1 + a) - y2
    # z3 = (y1 + a) * z2 - y3
    # ...
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


def main():
    # початкова точка в графі X = (x1, x2, ..., xN)
    char_ecncode_mod = 256
    chars = read_text_to_ascii("data2.txt", char_ecncode_mod)
    # список кроків d = [d1, d2, ..., ds]
    d_mod = 128
    d = [i for i in range(d_mod)]

    # print(chars)

    for a in d:
        if a % 2 == 0:
            chars = find_neigbors_N_a(chars, a, char_ecncode_mod)
            # print(chars, "Nx")
        else:
            chars = find_neigbors_M_a(chars, a, char_ecncode_mod)
            # print(chars, "My")

    encoded_text = text_from_int_to_ascii(chars)

    print(encoded_text)
    write_text_to_file("solution_task2.txt", encoded_text)


main()
