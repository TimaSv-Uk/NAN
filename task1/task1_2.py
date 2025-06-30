from itertools import product


def generate_matrix(mod=5, num_of_x=3):
    return [list(p) for p in product(range(mod), repeat=num_of_x)]


def build_adjacency_matrix(mod=5):
    matrix_X = generate_matrix(mod)
    matrix_Y = generate_matrix(mod)
    A = []
    print(matrix_Y)
    for x in matrix_X:
        row = []
        for y in matrix_Y:
            if ((x[1] + y[1]) % mod == (x[0] * y[0]) % mod) and (
                (x[2] + y[2]) % mod == (x[0] * y[1]) % mod
            ):
                row.append(1)
            else:
                row.append(0)
        A.append(row)
    return A


def build_full_matrix(A):
    size = len(A)
    # Build 16x16 matrix 4 blocks: O, A, At, O
    full_matrix = []

    for i in range(size):
        full_matrix.append([0 for _ in range(size)] + A[i])  # [O | A]
    for j in range(size):
        row = []
        for i in range(size):
            row.append(A[i][j])
        row += [0 for _ in range(size)]  # [At | O]
        full_matrix.append(row)
    return full_matrix



def print_labeled_matrix(matrix, filename=None):
    size = len(matrix) // 2
    lines = []

    header = "\t"
    for i in range(size):
        header += f"x{i + 1}\t"
    for i in range(size):
        header += f"y{i + 1}\t"
    lines.append(header)

    for i, row in enumerate(matrix):
        if i < size:
            label = f"x{i + 1}"
        else:
            label = f"y{i - size + 1}"
        row_str = "\t".join(str(v) for v in row)
        lines.append(f"{label}\t{row_str}")

    if filename:
        with open(filename, "w") as f:
            f.write("\n".join(lines))
    else:
        print("\n".join(lines))


def main():
    mod = 128
    A = build_adjacency_matrix(mod)
    full_matrix = build_full_matrix(A)

    print_labeled_matrix(full_matrix, "solution_task1_2.txt")

    print("\n--- FULL 16x16 ADJACENCY MATRIX ---\n")
    print_labeled_matrix(full_matrix)


main()
