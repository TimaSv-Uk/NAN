import galois
import numpy as np

# NOTE: the purpuse of this file is to test galois library

if __name__ == "__main__":
    GF = galois.GF(2**8)
    x = GF([236, 87, 38, 112])
    y = GF([109, 17, 108, 224])

    # Reset to the integer representation
    print(x)
    print(y)
    # The default is the integer representation
    GF.repr("poly")
    print(x.view(GF))
    GF.repr("power")
    print(x.view(GF))

    GF.repr("int")
    print(x + y)
    np.sqrt(x)

    # point_out[0] = point_in[0] + a_gf
    GF2 = galois.GF(2**2)

    x = GF2([2, 3])
    y = GF2([2, 1])
    print(x + y)
    print(x[0] + y[0])
