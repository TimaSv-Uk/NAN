import galois
import numpy as np


if __name__ == "__main__":
    GF = galois.GF(2**8)
    x = GF([236,  87,  38, 112])
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
    print(x+y)
    np.sqrt(x)
