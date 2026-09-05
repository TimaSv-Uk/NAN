- F8_MULT_BASED redo with SageMath library (polinomial part of the lib)
    - in polinomial out formula that allows only to encode, (public key concept)
x1,x2,xn => addition and multiplication => f_n(x1,x2,...,xn)
Graph coordinats, ring

x1,x2,x3  | c1,c2,c3 => get polinomial after SageMath calculations



# NOTES:
+ F8_MULT_BASED redo with SageMath library (polinomial part of the lib)
### Fot this i desided to use galois library insted of SageMath for a purpuse of definig explicit_polynomial insted of librarys default one
implemented as precompute_gf256_multiplication_explicit_poly() functoin

- in polinomial out formula that allows only to encode, (public key concept)
decode() walks backward through the same range, computing a_inv at each step and applying the inverse.
Both directions need the exact same seed — that's what produces the exact same d_mod_range, which is what lets decode()
know which a values to invert.
Anyone holding seed can do both operations.
This is a symmetric-key scheme — same secret unlocks both directions, structurally identical in spirit to AES.


# TODO TODAY:
**NOW TEST**
+ in polinomial out formula that allows only to encode, (public key concept)
    1. key(seed) to encode and decode must be difirent
        IDEA: encode operatin shoul return encoded bites with decode key,
        that person that shares encoded content will give to decoder

        - Pick a public/encode exponent e such that gcd(e, 255) = 1.
        - Compute the decode exponent d = e⁻¹ mod 255 — i.e. the number satisfying e · d ≡ 1 (mod 255).
        - Then (x^e)^d = x^(e·d) = x^1 = x. Encoding raises to e, decoding raises to d. Different numbers, mathematically paired, and one doesn't reveal the other without knowing 255's factorization and doing a modular inverse — cheap here since it's public math, but the structure is identical to RSA (which is exactly the same idea, just mod a huge composite where you don't know the factorization).

        NOTE:(d is computed from e via a formula (extended Euclidean algorithm))

    2. add  seperate functions, try not to change algo_classes
    3. add option to choose algo and toggle option to encode with key inside the desctop app
         

## PLAN FOR NOW:
 rather than patching F8_MULT_BASED: with y = x^e, decode literally only needs one number (d), not a whole reconstructed d_mod_range sequence that has to line up element-by-element with what encode used. Two options from here:

1. Swap the core algorithm to the power-map version (F8_EXP_BASED or similar) I sketched last message — encode_key → single exponent e, get_public_key → single exponent d, no d_mod_range sequence-matching problem at all.
or
2. Keep F8_MULT_BASED's structure but redefine what "key" means for it — e.g., derive the entire d_mod_range sequence from private_key, and derive a parallel sequence of per-element inverses (using get_public_key-style math on each element) as the "public" side, then feed that whole inverse sequence into decode() instead of re-deriving it from a scalar decode_key. More faithful to your original algorithm, but more moving parts.

(for now im in favor of 2)

### Reson why 
This means decode's correctness depends on decode() walking through the same d_mod_range sequence that encode() used (just in reverse, computing inverses as it goes) — it's inverting each a value, not inverting "the key." So if you call randomize_d_mod(d_mod, decode_key) with a different key than encode used, you get a completely different d_mod_range sequence, whose element-wise inverses have no relationship to encode's actual a values. It won't decode correctly — not because the key math is wrong, but because the algorithm was never designed to take "a different but related sequence" as input; it expects the same sequence.




