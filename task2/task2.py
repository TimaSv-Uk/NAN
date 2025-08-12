def encode(encoded_text_int: list[int], char_ecncode_mod: int, d_mod: int):
    d = [i for i in range(d_mod)]
    chars = encoded_text_int.copy()
    # print(encoded_text_int)
    nodes = [{"node": chars, "index": 0, "type": "X"}]
    for a in d:
        prev_chars = chars.copy()
        if a % 2 == 0:
            # print(f"a = {a},node = {prev_chars},next = N-X")
            chars = find_neigbors_N_a(chars, a, char_ecncode_mod)
            nodes.append({"nodes": chars, "index": a, "type": "N-X"})
        else:
            # print(f"a = {a},node = {prev_chars},next = M-X")
            chars = find_neigbors_M_a(chars, a, char_ecncode_mod)
            nodes.append({"nodes": chars, "index": a, "type": "M-Y"})
        if not follows_graph_rule(prev_chars, chars, char_ecncode_mod):
            print(f"Rule is broken at a={a}. For x ={prev_chars},y ={chars}")
            print(nodes[-2])
            print(nodes[-1])
            print("\n")
            # print(f"X: {prev_chars}")
            # print(f"Y: {chars}")
        else:

            print(f"Rule is not broken at a={a}. For x ={prev_chars},y ={chars}")
            print(nodes[-2])
            print(nodes[-1])
            print("\n")
            # print(f"X: {prev_chars}")
            # print(f"Y: {chars}")

    return chars


def decode(encoded_text_int: list[int], char_ecncode_mod: int, d_mod: int):
    chars = encoded_text_int.copy()
    for a in reversed(range(d_mod)):
        if a % 2 == 0:
            chars = reverce_find_neigbors_N_a(chars, a, char_ecncode_mod)
            # print(f"After reverse N_a({a}): {chars}")
        else:
            chars = reverce_find_neigbors_M_a(chars, a, char_ecncode_mod)
            # print(f"After reverse M_a({a}): {chars}")
    return chars


def find_neigbors_N_a(point, a, mod):
    """
    # N_a(X) = [x1+a, z2, z3, ..., zn]
    # де:
    # z2 = x1 * (x1 + a) - x2
    # z3 = x1 * z2 - x3
    # ...,
    # zn = x1 * z(n-1) - xn
    """
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


def get_change_first_symbol_based_on_full_vector(
    chars: list[int], char_ecncode_mod: int
) -> list[int]:
    """
    Calculates a new value for the first character in 'text' based on a weighted sum
    of all characters' modulo values, then applies 'char_ecncode_mod' to the result.

    Args:
        text (str): The input string.
        char_ecncode_mod (int): The modulus for character encoding and final calculation.

    Returns:
        list[int]: A list of integers with the modified first character's value
                   and the original modulo values for the rest.
    """
    new_chars = list(chars)
    # Make sure there are at least 2 elements
    if len(new_chars) < 2:
        return new_chars

    M = 1
    for char_val in new_chars[1:]:
        M *= 2 * char_val + 1
        M %= char_ecncode_mod

    original_first_char_val = (new_chars[0] * M) % char_ecncode_mod
    new_chars[0] = original_first_char_val

    return new_chars


def reverse_change_first_symbol_based_on_full_vector(
    chars: list[int], char_ecncode_mod: int
) -> list[int]:
    """
    Why the inverse always exists
    For any integer xi, 2 * xi is even.
    So, 2 * xi + 1 is always odd.

    M = (2 * x2 + 1) * (2 * x3+1) ... (2 * xn+1)

    x1' => x1 * M
    x1 = x1' / M
    """
    new_chars = list(chars)
    # Make sure there are at least 2 elements
    if len(new_chars) < 2:
        return new_chars

    M = 1
    for char_val in new_chars[1:]:
        M *= 2 * char_val + 1
        M %= char_ecncode_mod

    try:
        M_inv = pow(M, -1, char_ecncode_mod)
    except ValueError:
        raise ValueError(f"M = {M} has no modular inverse modulo {char_ecncode_mod}")

    original_first_char_val = (new_chars[0] * M_inv) % char_ecncode_mod
    new_chars[0] = original_first_char_val

    return new_chars


# TODO: assignment5


def encode_assignment5(encoded_text_int: list[int], char_ecncode_mod: int, d_mod: int):
    d = [i for i in range(d_mod)]
    chars = encoded_text_int.copy()
    # print(encoded_text_int)
    for a in d:
        chars = find_neighbors_assignment5(chars, a, char_ecncode_mod)
        # print(chars, "My")
    return chars


def find_neighbors_assignment5(point, a, mod):
    """
    # New N_a for new equation rules
    # N_a(X) = [x1+a, z2, z3, ..., zn]
    # Even (math index) => y1*x_{i-1}, Odd => x1*y_{i-1}
    """
    point = point.copy()
    neighbor_point = []

    for i in range(len(point)):
        if i == 0:
            # math index 1
            x1_new = (point[0] + a) % mod
            neighbor_point.append(x1_new)
        elif i % 2 == 0:
            # math index even → use y1 * prev_x
            z_i = (
                point[0] * neighbor_point[-1] - point[i]
            ) % mod  # y1 is point[0] in M, but here?
            neighbor_point.append(z_i)
        else:
            # math index odd → use x1 * prev_y
            z_i = (point[0] * neighbor_point[-1] - point[i]) % mod
            neighbor_point.append(z_i)
    return neighbor_point


def follows_graph_rule(x: list[int], y: list[int], mod: int) -> bool:
    """
    (x1,x2,...,xn) [y1,y2,...,yn]

    x2+y2= x1*y1
    x3+y3 = x1*y2
    x4+y4 = x1*y3
    ....
    xn+yn = x1*yn-1
    """
    n = len(x)
    for k in range(1, n):  # k = 1..n-1 бо індексація з 0
        if (x[k] + y[k]) % mod != (x[0] * y[k - 1]) % mod:
            return False
    return True


# TODO:


def follows_graph_rule_assignment5(x: list[int], y: list[int], mod: int) -> bool:
    """
    (х_х1, х_2,..., х_п) і [у_1,у_2,..., у_п) коли

    х_2 - у_2 = у_1х_1
    х_3 - у_3 = х_1у_2
    х_4 - у_4 = у_1х_3
    х_5 - у_5 = х_1у_4

    х_6 - у_6 = у_1х_5
    х_7 - у_7 = х_1у_6
    ...
    х_п - у_п = (х_1у_п-1 або у_1х_п-1 в залежності від того, парне п чи непарне).
    """
    n = len(x)
    for k in range(1, n):  # k = 1..n-1 бо індексація з 0
        if k % 2 == 0:
            if (x[k] - y[k]) % mod != (y[0] * x[k - 1]) % mod:
                return False
        else:
            if (x[k] - y[k]) % mod != (x[0] * y[k - 1]) % mod:
                return False
    return True


def main():
    char_ecncode_mod = 128
    d_mod = 10
    text = [0 for i in range(10)]
    encoded = encode(text, char_ecncode_mod, d_mod)

    # Збільшити граф
    # (x1,x2,...,xn) [y1,y2,...,yn]
    #
    # x2+y2= x1*y1
    # x3+y3 = x1*y2
    # x4+y4 = x1*y3
    # ....
    # xn+yn = x1*yn-1


if __name__ == "__main__":
    main()
