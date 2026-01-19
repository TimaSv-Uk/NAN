import csv

# ==========================================
# CONFIGURATION (CHANGE THIS)
# ==========================================

# 1. Choose the size of the field (n)
#    3 for 2^3 (8 elements)
#    8 for 2^8 (256 elements)
FIELD_DEGREE = 3

# 2. Choose the rule (Irreducible Polynomial)
#    Input the full binary representation of the polynomial.
#
#    EXAMPLE A: for x^3 = x + 1 (your request)
#    Polynomial is: x^3 + x + 1
#    Binary:        1     0   1   1  -> 0b1011 (or 11 or 0xB)
#
#    EXAMPLE B: for x^8 = x + 1 (your previous request)
#    Polynomial is: x^8 + x + 1
#    Binary:        1 000000 1 1     -> 0b100000011 (or 259 or 0x103)
#
#    EXAMPLE C: for AES Standard (x^8 + x^4 + x^3 + x + 1)
#    Binary:        1 0001 1011      -> 0b100011011 (or 283 or 0x11B)

IRREDUCIBLE_POLY = 0b1011  # Currently set to x^3 + x + 1

# ==========================================
#  AUTOMATIC CALCULATIONS (DO NOT TOUCH)
# ==========================================

FIELD_SIZE = 1 << FIELD_DEGREE      # e.g., 8 for degree 3
MSB_MASK = 1 << (FIELD_DEGREE - 1)  # The Most Significant Bit (e.g., 4 for degree 3)
# The "Mask" is the polynomial without the top bit (used for XORing)
POLY_MASK = IRREDUCIBLE_POLY & (FIELD_SIZE - 1) 

def to_poly_str(val):
    """Converts a number to a polynomial string (e.g., 3 -> x + 1)."""
    if val == 0: return "0"
    if val == 1: return "1"
    
    terms = []
    # Scan bits from the highest possible power down to 0
    for i in range(FIELD_DEGREE - 1, -1, -1):
        if (val >> i) & 1:
            if i == 0: terms.append("1")
            elif i == 1: terms.append("x")
            else: terms.append(f"x^{i}")
    return " + ".join(terms)

def multiply(a, b):
    """Universal multiplication for GF(2^n)."""
    p = 0
    # Loop exactly n times (where n is the degree)
    for i in range(FIELD_DEGREE):
        # 1. If the last bit of b is 1, add a to the product
        if (b & 1):
            p ^= a
        
        # 2. Check if 'a' is about to overflow the field size
        high_bit_set = (a & MSB_MASK)
        
        # 3. Shift 'a' to the left (multiply by x)
        a <<= 1
        
        # 4. If it overflowed, subtract (XOR) the polynomial modulus
        if high_bit_set:
            a ^= IRREDUCIBLE_POLY
            
        # Ensure 'a' stays within the field bit-width (removes the overflow bit)
        a &= (FIELD_SIZE - 1)
            
        b >>= 1
        
    return p

def generate_file():
    filename = f"gf_2_{FIELD_DEGREE}_table.csv"
    print(f"Generating table for GF(2^{FIELD_DEGREE}) with Poly {bin(IRREDUCIBLE_POLY)}...")
    print(f"Field Size: {FIELD_SIZE}")
    print(f"Output file: {filename}")
    
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        
        # Headers
        headers = ["*"] + [to_poly_str(i) for i in range(FIELD_SIZE)]
        writer.writerow(headers)
        
        # Rows
        for row_idx in range(FIELD_SIZE):
            row_poly = to_poly_str(row_idx)
            row_data = [row_poly]
            
            for col_idx in range(FIELD_SIZE):
                res_val = multiply(row_idx, col_idx)
                row_data.append(to_poly_str(res_val))
            
            writer.writerow(row_data)
            
            if row_idx > 0 and row_idx % 50 == 0:
                print(f"Processed: {row_idx}/{FIELD_SIZE}")

    print("Done!")

if __name__ == "__main__":
    generate_file()
