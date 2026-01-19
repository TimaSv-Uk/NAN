import csv


def to_poly_str(val):
    """
    Перетворює число у рядок полінома.
    Наприклад: 3 -> "x + 1", 7 -> "x^2 + x + 1"
    """
    if val == 0:
        return "0"
    if val == 1:
        return "1"
    terms = []
    # Перевіряємо біти від 7 до 0 (оскільки це 2^8)
    for i in range(7, -1, -1):
        if (val >> i) & 1:
            if i == 0:
                terms.append("1")
            elif i == 1:
                terms.append("x")
            else:
                terms.append(f"x^{i}")
    return " + ".join(terms)


def multiply(a, b, poly_mod_mask=0x03):
    """
    Множення у полі GF(2^8) за правилом x^8 = x + 1.
    poly_mod_mask = 0x03 відповідає (x + 1)
    """
    p = 0
    for i in range(8):
        # Якщо останній біт b - одиниця, додаємо a до результату
        if b & 1:
            p ^= a

        # Перевірка на переповнення (чи є біт x^7 перед зсувом)
        high_bit_set = a & 0x80

        # Зсув вліво (множення на x)
        a = (a << 1) & 0xFF  # Обмежуємо 8 бітами

        # Якщо було переповнення (x^8), робимо XOR з поліномом (x + 1)
        if high_bit_set:
            a ^= poly_mod_mask

        b >>= 1
    return p


def generate_file(filename="gf_2_8_table.csv"):
    print(f"Генерація таблиці у файл '{filename}'...")

    size = 256  # 2^8

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        # 1. Заголовки (верхній рядок)
        headers = ["*"] + [to_poly_str(i) for i in range(size)]
        writer.writerow(headers)

        # 2. Тіло таблиці
        for row_idx in range(size):
            row_poly = to_poly_str(row_idx)
            row_data = [row_poly]  # Перша колонка - множник

            for col_idx in range(size):
                res_val = multiply(row_idx, col_idx)
                row_data.append(to_poly_str(res_val))

            writer.writerow(row_data)

            # Вивід прогресу кожні 50 рядків
            if row_idx % 50 == 0:
                print(f"Оброблено рядків: {row_idx}/{size}")

    print("Готово! Файл успішно створено.")


# Запуск генерації
if __name__ == "__main__":
    generate_file()
import csv


def to_poly_str(val):
    """
    Перетворює число у рядок полінома.
    Наприклад: 3 -> "x + 1", 7 -> "x^2 + x + 1"
    """
    if val == 0:
        return "0"
    if val == 1:
        return "1"
    terms = []
    # Перевіряємо біти від 7 до 0 (оскільки це 2^8)
    for i in range(7, -1, -1):
        if (val >> i) & 1:
            if i == 0:
                terms.append("1")
            elif i == 1:
                terms.append("x")
            else:
                terms.append(f"x^{i}")
    return " + ".join(terms)


def multiply(a, b, poly_mod_mask=0x03):
    """
    Множення у полі GF(2^8) за правилом x^8 = x + 1.
    poly_mod_mask = 0x03 відповідає (x + 1)
    """
    p = 0
    for i in range(8):
        # Якщо останній біт b - одиниця, додаємо a до результату
        if b & 1:
            p ^= a

        # Перевірка на переповнення (чи є біт x^7 перед зсувом)
        high_bit_set = a & 0x80

        # Зсув вліво (множення на x)
        a = (a << 1) & 0xFF  # Обмежуємо 8 бітами

        # Якщо було переповнення (x^8), робимо XOR з поліномом (x + 1)
        if high_bit_set:
            a ^= poly_mod_mask

        b >>= 1
    return p


def generate_file(filename="gf_2_8_table.csv"):
    print(f"Генерація таблиці у файл '{filename}'...")

    size = 256  # 2^8

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        # 1. Заголовки (верхній рядок)
        headers = ["*"] + [to_poly_str(i) for i in range(size)]
        writer.writerow(headers)

        # 2. Тіло таблиці
        for row_idx in range(size):
            row_poly = to_poly_str(row_idx)
            row_data = [row_poly]  # Перша колонка - множник

            for col_idx in range(size):
                res_val = multiply(row_idx, col_idx)
                row_data.append(to_poly_str(res_val))

            writer.writerow(row_data)

            # Вивід прогресу кожні 50 рядків
            if row_idx % 50 == 0:
                print(f"Оброблено рядків: {row_idx}/{size}")

    print("Готово! Файл успішно створено.")


# Запуск генерації
if __name__ == "__main__":
    generate_file()
