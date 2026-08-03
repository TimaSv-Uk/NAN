import numpy as np
from numba import njit


from ...precompute_multiplication import load_gf256

from ..base import BaseEncodeDecodeAlgorithm
from ..finite_field import F8


class F8_MULT_BASED(F8):
    """
    Based on finite_field algorithm. Main deviation from the base F8 algorithm 
    is the initialization step, which uses Galois Field GF(2^8) multiplication: 
    y_0 = x_0 * a.

    The subsequent elements are calculated using Galois Field GF(2^8) arithmetic 
    (where subtraction/addition is evaluated as XOR) according to the following rules:
      х_2 - у_2 = у_1 * х_1   =>   у_2 = х_2 ^ (у_1 * х_1)
      х_3 - у_3 = х_1 * у_2   =>   у_3 = х_3 ^ (х_1 * у_2)
      х_4 - у_4 = у_1 * х_3   =>   у_4 = х_4 ^ (у_1 * х_3)
      х_5 - у_5 = х_1 * у_4   =>   у_5 = х_5 ^ (х_1 * у_4)
    """

    def encode(self) -> np.ndarray:
        # Use standard uint8 arrays
        current_state = self.chars.astype(np.uint8)
        next_state = np.zeros_like(current_state)

        for a in self.d_mod_range:
            # Catch 0 and force it to 1
            a = np.uint8(1) if a == 0 else np.uint8(a)
            self._find_neighbors(current_state, next_state, a, self.mul_lut)

            temp = current_state
            current_state = next_state
            next_state = temp

        return current_state
    def decode(self) -> np.ndarray:
        current_state = self.chars.astype(np.uint8)
        next_state = np.zeros_like(current_state)

        for i in range(len(self.d_mod_range) - 1, -1, -1):
            a_raw = self.d_mod_range[i]
            # Catch 0 and force it to 1 for consistency with encoding
            a = np.uint8(1) if a_raw == 0 else np.uint8(a_raw)

            # Calculate the multiplicative inverse of 'a' using the lookup table.
            # We find the index where multiplying 'a' by that index equals 1.
            # NOTE:
            # The mathematical number 0 does not have a multiplicative inverse in GF(2^8).
            # If a is 0, the line np.where(self.mul_lut[a] == 1)[0][0]
            # will throw an IndexError because there is no value in row 0 that equals 1.
            # Make sure your d_mod_range only generates bytes from 1 to 255.
            a_inv = np.where(self.mul_lut[a] == 1)[0][0]

            self._reverse_find_neighbors(current_state, next_state, a_inv, self.mul_lut)

            temp = current_state
            current_state = next_state
            next_state = temp

        return current_state

    @staticmethod
    @njit
    def _find_neighbors(
        point_in: np.ndarray, point_out: np.ndarray, a: int, mul_lut: np.ndarray
    ) -> None:
        n = len(point_in)

        # NOTE: Reverse initial rule: x0 = y0 * (a^-1). Main deviation from base F8 algorithm
        point_out[0] = mul_lut[point_in[0], a]

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
        point_in: np.ndarray, point_out: np.ndarray, a_inv: int, mul_lut: np.ndarray
    ) -> None:
        n = len(point_in)

        # x0 = y0 - a -> Subtraction is also XOR (^)
        # Reverse initial rule: x0 = y0 * (a^-1) -> Lookup multiplication of y0 and a_inv
        point_out[0] = mul_lut[point_in[0], a_inv]

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
