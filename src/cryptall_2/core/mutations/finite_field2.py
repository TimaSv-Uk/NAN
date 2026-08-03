import numpy as np
from numba import njit


from ...precompute_multiplication import load_gf256

from ..base import BaseEncodeDecodeAlgorithm


class F8(BaseEncodeDecodeAlgorithm):
    """
    Third algorithm that was implemented, based on finite_field operations insted of modulo
    """

    def __init__(self, chars: np.ndarray, d_mod_range: np.ndarray):
        self.chars = chars
        self.d_mod_range = d_mod_range
        self.mul_lut = load_gf256("multiplication_table/mul_gf256.npy")

    def encode(self) -> np.ndarray:
        # Use standard uint8 arrays
        current_state = self.chars.astype(np.uint8)
        next_state = np.zeros_like(current_state)

        for a in self.d_mod_range:
            self._find_neighbors(current_state, next_state, np.uint8(a), self.mul_lut)

            temp = current_state
            current_state = next_state
            next_state = temp

        return current_state

    def decode(self) -> np.ndarray:
        current_state = self.chars.astype(np.uint8)
        next_state = np.zeros_like(current_state)

        for i in range(len(self.d_mod_range) - 1, -1, -1):
            a = np.uint8(self.d_mod_range[i])
            self._reverse_find_neighbors(current_state, next_state, a, self.mul_lut)

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

        # y0 = x0 + a -> Addition is XOR (^)
        point_out[0] = point_in[0] ^ a

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

        # x0 = y0 - a -> Subtraction is also XOR (^)
        point_out[0] = point_in[0] ^ a

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
