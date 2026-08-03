import numpy as np
from numba import njit


from ...precompute_multiplication import load_gf256

from ..base import BaseEncodeDecodeAlgorithm
from ..finite_field import F8


class F8_ADDITION_BASED(F8):
    """
    Based on finite_field algorithm. Main deviation from the base F8 algorithm 
    is the initialization step, which uses standard modulo 256 addition: 
    y_0 = (x_0 + a) % 256.

    The subsequent elements are calculated using Galois Field GF(2^8) arithmetic 
    (where subtraction/addition is evaluated as XOR) according to the following rules:
      х_2 - у_2 = у_1 * х_1   =>   у_2 = х_2 ^ (у_1 * х_1)
      х_3 - у_3 = х_1 * у_2   =>   у_3 = х_3 ^ (х_1 * у_2)
      х_4 - у_4 = у_1 * х_3   =>   у_4 = х_4 ^ (у_1 * х_3)
      х_5 - у_5 = х_1 * у_4   =>   у_5 = х_5 ^ (х_1 * у_4)
    """

    @staticmethod
    @njit
    def _find_neighbors(
        point_in: np.ndarray, point_out: np.ndarray, a: int, mul_lut: np.ndarray
    ) -> None:
        n = len(point_in)

        # NOTE: Reverse initial rule: x0 = (y0 - a) mod 256. Main deviation from base F8 algorithm
        point_out[0] = (point_in[0] + a) % 256

        x0 = point_in[0]
        y0 = point_out[0]

        for i in range(1, n):
            # i % 2 != 0 catches odd indices: 1, 3, 5... (Math elements x_2, x_4, x_6)
            if i % 2 != 0:
                # Rule: x_2 - y_2 = y_1 * x_1 => y_2 = x_2 + (y_1 * x_1)
                point_out[i] = point_in[i] ^ mul_lut[y0, point_in[i - 1]]

            # i % 2 == 0 catches even indices: 2, 4, 6... (Math elements x_3, x_5, x_7)
            else:
                # Rule: x_3 - y_3 = x_1 * y_2 => y_3 = x_3 + (x_1 * y_2)
                point_out[i] = point_in[i] ^ mul_lut[x0, point_out[i - 1]]

    @staticmethod
    @njit
    def _reverse_find_neighbors(
        point_in: np.ndarray, point_out: np.ndarray, a: int, mul_lut: np.ndarray
    ) -> None:
        n = len(point_in)


        # NOTE: Reverse initial rule: x0 = (y0 + a) mod 256. Main deviation from base F8 algorithm
        point_out[0] = (point_in[0] - a) % 256

        x0 = point_out[0]
        y0 = point_in[0]

        for i in range(1, n):
            # i % 2 != 0 catches odd indices: 1, 3, 5... (Math elements x_2, x_4, x_6)
            if i % 2 != 0:
                # Rule: x_2 = y_2 + (y_1 * x_1)
                # x_{i} = y_{i} ^ (y0 * x_{i-1})
                point_out[i] = point_in[i] ^ mul_lut[y0, point_out[i - 1]]

            # i % 2 == 0 catches even indices: 2, 4, 6... (Math elements x_3, x_5, x_7)
            else:
                # Rule: x_3 = y_3 + (x_1 * y_2)
                # x_{i} = y_{i} ^ (x0 * y_{i-1})
                point_out[i] = point_in[i] ^ mul_lut[x0, point_in[i - 1]]
