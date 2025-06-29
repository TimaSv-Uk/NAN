import numpy as np

# Ваша матриця A (8x8) — як список списків або numpy array
A = [
    [1, 0, 0, 0, 1, 0, 0, 0],
    [0, 1, 0, 0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0, 0, 1, 0],
    [0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [0, 1, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 1, 1, 0, 0, 0],
    [0, 0, 1, 0, 0, 1, 0, 0],
]

A = np.array(A)
zero_block = np.zeros_like(A)

# Збираємо повну матрицю суміжності 16x16
top = np.hstack([zero_block, A])
bottom = np.hstack([A.T, zero_block])
full_matrix = np.vstack([top, bottom])

# Вивід для перевірки
for row in full_matrix:
    print("\t".join(str(x) for x in row))
