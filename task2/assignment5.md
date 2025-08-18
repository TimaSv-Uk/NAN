
# Модіфікований алгоритм (Assignment 5)

Для розширення можливостей побудови графа додано нове правило знаходження сусідів, яке визначає, як із початкового вектора

    (х_х1, х_2,..., х_п) і [у_1,у_2,..., у_п) коли

    х_2 - у_2 = у_1х_1
    х_3 - у_3 = х_1у_2
    х_4 - у_4 = у_1х_3
    х_5 - у_5 = х_1у_4

    х_6 - у_6 = у_1х_5
    х_7 - у_7 = х_1у_6

## Зворотний перехід X → Y

Для першої координати:

    index 1: y1 = x1 + a

Для парних індексів (математично парні, тобто i = 2, 4, 6, ...):

    even math index: y_i = x_i - (y1 * x_{i-1})

Для непарних індексів (i = 3, 5, 7, ...):

    odd math index: y_i = x_i - (x1 * y_{i-1})


## Зворотний перехід Y → X

Для першої координати:

    index 1: x1 = y1 - a

Для парних індексів (математично парні, тобто i = 2, 4, 6, ...):

    even math index: x_i = y_i + y1 * x_{i-1}

Для непарних індексів (i = 3, 5, 7, ...):

    odd math index: x_i = y_i + x1 * y_{i-1}



У коді за це відповідають функції:
```
/task2.py

def decode_assignment5(
    encoded_text_int: list[int], char_ecncode_mod: int, d_mod: int
) -> list[int]:

def encode_assignment5(
    encoded_text_int: list[int], char_ecncode_mod: int, d_mod: int
) -> list[int]:

def find_neighbors_assignment5(point, a, mod)

def reverse_find_neighbors_assignment5(point, a, mod):

```
