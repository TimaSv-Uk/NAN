import csv

def to_poly_str(val):
    """
    Для GF(2^3): числа від 0 до 7
    """
    if val == 0: return "0"
    if val == 1: return "1"
    
    terms = []
    # Перевіряємо лише 3 біти (2, 1, 0), бо це 2^3
    for i in range(2, -1, -1):
        if (val >> i) & 1:
            if i == 0: terms.append("1")
            elif i == 1: terms.append("x")
            else: terms.append(f"x^{i}")
    return " + ".join(terms)

def multiply(a, b):
    """
    Множення для GF(2^3) з правилом x^3 = x + 1.
    """
    p = 0
    # Маска полінома: x+1 це '011' -> 0x03
    poly_mod_mask = 0x03 
    
    # Проходимо по 3 бітах (ступінь поля = 3)
    for i in range(3):
        # 1. Додавання
        if (b & 1):
            p ^= a
        
        # 2. Перевірка: чи є у 'a' біт x^2 (це 3-й біт, значення 4 -> 100)
        # Якщо він є, то після зсуву він стане x^3, що вимагає модульного ділення
        high_bit_set = (a & 0x04) 
        
        # 3. Зсув (множення на x)
        a <<= 1
        
        # 4. Якщо вилізли за межі x^2 (стали x^3), робимо XOR з (x+1)
        if high_bit_set:
            a ^= poly_mod_mask
        
        # Обрізаємо все, що більше 3 біт (для безпеки), хоча логіка вище це гарантує
        a &= 0x07 
            
        b >>= 1
        
    return p & 0x07

def generate_file(filename="gf_2_3_table.csv"):
    print(f"Генерація таблиці для GF(2^3) [x^3 = x + 1] у '{filename}'...")
    
    # Розмір поля 2^3 = 8
    size = 8 
    
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        
        # Заголовки
        headers = ["*"] + [to_poly_str(i) for i in range(size)]
        writer.writerow(headers)
        
        # Тіло таблиці
        for row_idx in range(size):
            row_poly = to_poly_str(row_idx)
            row_data = [row_poly]
            
            for col_idx in range(size):
                res_val = multiply(row_idx, col_idx)
                row_data.append(to_poly_str(res_val))
            
            writer.writerow(row_data)

    print("Готово! Таблиця 8x8 створена.")

if __name__ == "__main__":
    generate_file()
