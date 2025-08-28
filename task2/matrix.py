import numpy as np
import time


def matrix_vector_mult(matrix, vector):
    new_vector = []
    for row in matrix:
        sum = 0
        for index, item in enumerate(row):
            sum += item * vector[index]
        new_vector.append(sum)
    return new_vector


def vector_matrix_mult(vector, matrix):
    new_vector = []

    for i in range(len(vector)):
        sum = 0
        for j in range(len(matrix[i])):
            sum += vector[j] * matrix[j][i]
        new_vector.append(sum)
    return new_vector


def main():
    # chars = [i for i in range(10)]
    # seed = 42
    # mod = 258
    # shape (3,) works like a column vector here
    vector = [3, 1, 2]
    matrix = [[1, 1, 2], [2, 1, 3], [1, 4, 2]]

    start_time = time.perf_counter()
    print(matrix_vector_mult(matrix, vector))
    print(vector_matrix_mult(vector, matrix))
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    print(execution_time)

    vector = np.array([3, 1, 2])
    matrix = np.array([[1, 1, 2], [2, 1, 3], [1, 4, 2]])
    start_time = time.perf_counter()
    print((matrix @ vector) % 2)
    print((vector @ matrix) % 2)
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    print(execution_time)


if __name__ == "__main__":
    main()
