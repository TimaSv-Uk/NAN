from itertools import product, batched


def generate_matrix(mod=2, num_of_x=3):
    # product(range(mod), repeat=num_of_x) generates all possible tuples of length num_of_x,
    # where each element is from 0 to mod - 1.
    return [list(p) for p in product(range(mod), repeat=num_of_x)]


def main():
    adjasonsy_matrix = []
    # print(generate_matrix())
    matrix_X = generate_matrix(2, 3)
    matrix_Y = generate_matrix(2, 3)

    for x in matrix_X:
        for y in matrix_Y:
            if ((x[1] + y[1]) % 2 == (x[0] * y[0]) % 2) and (
                (x[2] + y[2]) % 2 == (x[0] * y[1]) % 2
            ):
                adjasonsy_matrix.append([x, y, 1])
                # print(x,y)
            else:
                adjasonsy_matrix.append([x, y, 0])
    # x2 + y2 = x1 * y1
    # x3 + y3 = x1 * y2
    solution_matrix = list(batched([element[2] for element in adjasonsy_matrix], 8))
    print(solution_matrix)

    f = open("solution_task1_2.txt", "w")

    f.write("   ")
    for i, _ in enumerate(solution_matrix):
        f.write(f"y{i + 1} ")

    f.write("\n")
    for i, col in enumerate(solution_matrix):
        f.write(f"x{i + 1} ")
        for element in col:
            f.write(str(element) + "  ")

        f.write("\n")

    return


main()
