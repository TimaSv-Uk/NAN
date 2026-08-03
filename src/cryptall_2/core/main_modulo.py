import numpy as np
from numba import njit

import os

from .base import BaseEncodeDecodeAlgorithm
# NOTE:
# np.uint8 used inted of  modulo operation only works with  mod 256

# NOTE:
# val = (x * y) & mod  # instead of % 256,
# only works if your modulus is a power of two


class V5(BaseEncodeDecodeAlgorithm):
    """
    First algorithm that was implemented, initialy called v5
    """

    def __init__(
        self, chars: np.ndarray, char_encode_mod: int, d_mod_range: np.ndarray
    ):
        self.chars = chars
        self.char_encode_mod = char_encode_mod
        self.d_mod_range = d_mod_range

    def encode(self) -> np.ndarray:
        """
        # (х_х1, х_2,..., х_п) і [у_1,у_2,..., у_п) коли
        #
        # х_2 - у_2 = у_1х_1
        # х_3 - у_3 = х_1у_2
        # х_4 - у_4 = у_1х_3
        # х_5 - у_5 = х_1у_4
        #
        # х_6 - у_6 = у_1х_5
        # х_7 - у_7 = х_1у_6
        #
        # y_1 = x_1+a1
        # y2 = x2 - ( (x_1+a1) * x1 )
        # y3 = x3 - (х_1 у_2)
        # Наш початковий вектор це X тобто всі Х відомі Треба знайти Y (сусідa) за
            формулою та використати його в якості X за модулем.
        """
        current_state = self.chars.astype(np.uint8).copy()
        next_state = np.empty_like(current_state)

        for a in self.d_mod_range:
            self._find_neighbors(current_state, next_state, a, self.char_encode_mod)

            current_state, next_state = next_state, current_state

        return current_state

    def decode(self) -> np.ndarray:
        """
        # (х_х1, х_2,..., х_п) і [у_1,у_2,..., у_п) коли
        #
        # х_2 - у_2 = у_1х_1
        # х_3 - у_3 = х_1у_2
        # х_4 - у_4 = у_1х_3
        # х_5 - у_5 = х_1у_4
        #
        # х_6 - у_6 = у_1х_5
        # х_7 - у_7 = х_1у_6
        #

        x_1 = y_1-a1
        x2 = y2 + ( (x_1+a1) * x1 )
        x3 = y3 + (х_1 у_2)
        x4 = y4 + (y_1 x_3)
        # Наш початковий вектор це X тобто всі Х відомі Треба знайти Y (сусідa) за
          формулою та використати його в якості X за модулем.
        """

        current_state = self.chars.astype(np.uint8).copy()
        next_state = np.empty_like(current_state)
        # Replace reversed(range(d_mod)) with a backward range for @jit

        for i in range(len(self.d_mod_range) - 1, -1, -1):
            a = self.d_mod_range[i]
            self._reverse_find_neighbors(
                current_state, next_state, a, self.char_encode_mod
            )
            current_state, next_state = next_state, current_state  # Swap

        return current_state

    @staticmethod
    @njit
    def _find_neighbors(
        point_in: np.ndarray, point_out: np.ndarray, a: int, mod: int
    ) -> None:
        """
        point_in = (x1, x2, x3, ...)
        get Y node from X

        # index 1: y1 = x1 + a
        # even math index: y_i = x_i - (y1 * x_{i-1})
        # odd math index: y_i = x_i - (x1 * y_{i-1})

        """
        n = len(point_in)
        point_out[0] = (point_in[0] + a) % mod
        x0 = point_in[0]

        # NOTE:
        # val = (x) & mod  # instead of % 258, only works if your modulus is a power of two
        # automaticli aply mod 256 is use uint8
        for i in range(1, n):
            if i % 2 == 0:
                point_out[i] = np.uint8(point_in[i] - point_out[0] * point_in[i - 1])
                # temp = (point_in[i] - point_out[0] * point_in[i - 1])
                # point_out[i] = temp % mod
                # point_out[i] = temp & mod
            else:
                point_out[i] = np.uint8(point_in[i] - x0 * point_out[i - 1])
                # temp = (point_in[i] - x0 * point_out[i - 1])
                # point_out[i] = temp % mod
                # point_out[i] = temp & mod
        return None

    @staticmethod
    @njit
    def _reverse_find_neighbors(
        point_in: np.ndarray, point_out: np.ndarray, a: int, mod: int
    ) -> None:
        """
        point_in = [y1, y2, y3, ...]
        get X node from Y

        # index 1: x1 = y1 - a
        # even math index: x_i = y_i + y1 * x_{i-1}
        # odd math index: x_i = y_i + x1 * y_{i-1}

        """
        n = len(point_in)
        # point_out[0] = point_in[0] - a
        point_out[0] = (point_in[0] - a) % mod
        x0 = point_out[0]  # x1 is from the new array
        y0 = point_in[0]  # y1 is from the input array

        # NOTE:
        # np.uint8 used inted of  modulo operation only works with  mod 256
        # val = (x) & mod  # instead of % 258, only works if your modulus is a power of two
        # automaticli aply mod 256 is use uint8

        for i in range(1, n):
            if i % 2 == 0:
                point_out[i] = np.uint8(point_in[i] + y0 * point_out[i - 1])
                # point_out[i] = temp % mod
                # point_out[i] = temp & mod
            else:
                point_out[i] = np.uint8(point_in[i] + x0 * point_in[i - 1])
                # point_out[i] = temp % mod
                # point_out[i] = temp & mod
        return None


class V5_WITH_TABLE(BaseEncodeDecodeAlgorithm):
    """
    This is the version of First algorithm(v5),
    """

    def __init__(self, chars: np.ndarray, char_encode_mod: int, d_mod: int):
        self.chars = chars
        self.char_encode_mod = char_encode_mod
        self.d_mod = d_mod

    def encode(self):
        BASE_DIR = os.path.dirname(__file__)
        mul_table_path = os.path.join(
            BASE_DIR, "multiplication_table", f"mul_mod_{self.char_encode_mod}.npy"
        )
        mul_table = np.load(mul_table_path)
        mul_table = mul_table.astype(np.uint16)  # optional for speed & memory

        current_state = self.chars.copy()
        next_state = np.empty_like(current_state)
        for a in range(self.d_mod):
            self._find_neighbors(
                current_state, next_state, a, self.char_encode_mod, mul_table
            )
            current_state, next_state = next_state, current_state
        return current_state

    @staticmethod
    @njit
    def _find_neighbors(
        point_in: np.ndarray, point_out: np.ndarray, a: int, mod: int, mul_table
    ) -> None:
        """
        Calculates the next state and writes it into the pre-allocated
        point_out array.
        This version uses the precomputed multiplication table.

        point_in: The input array (X vector)
        point_out: The output array (Y vector)
        """
        n = len(point_in)

        # Calculate the first element (y1) and write it to the output array
        point_out[0] = (point_in[0] + a) % mod

        # Store x1 and y1 for reuse in the loop
        x0 = point_in[0]
        y0 = point_out[0]

        for i in range(1, n):
            if i % 2 == 0:
                # Even math index: y_i = x_i - (y1 * x_{i-1})
                # Use the multiplication table for y1 * x_{i-1}
                mult_result = mul_table[y0, point_in[i - 1]]
                point_out[i] = point_in[i] - mult_result
                # point_out[i] = temp % mod
                # point_out[i] = temp & mod
            else:
                # Odd math index: y_i = x_i - (x1 * y_{i-1})
                # Use the multiplication table for x1 * y_{i-1}
                mult_result = mul_table[x0, point_out[i - 1]]
                point_out[i] = point_in[i] - mult_result
                # point_out[i] = temp % mod
                # point_out[i] = temp & mod

    def decode(
        self,
    ) -> np.ndarray:
        raise NotImplementedError()

    @staticmethod
    def _reverse_find_neighbors() -> None:
        raise NotImplementedError()


class V10(BaseEncodeDecodeAlgorithm):
    """
    UNFINISHED

    Second algorithm that was implemented, initialy called v10
    This one does not have seperation of encode and find _find_neighbors functions, and is unfinished
    """

    #  def __init__(
    #      self, chars: np.ndarray, char_encode_mod: int, d_mod_range: np.ndarray, m: int
    #  ):
    #      self.chars = chars
    #      self.char_encode_mod = char_encode_mod
    #      self.d_mod_range = d_mod_range
    #      self.m = m

    @staticmethod
    @njit
    def encode(
        chars: np.ndarray, char_encode_mod: int, d_mod_range: np.ndarray, m: int
    ) -> np.ndarray:
        """
        improved version
        * from assighment5 graph algorithm

         (x1 x2 x3) [y1 = x1^m + a1, y2 = *,y3 = *]

         (y1 = x1 + a1 + a2, y2 = *,y3 = *)

         [y1 = x1^m + a1 + a2 + a3]

         (y1 = x1 + a1 + a2 + a3 + a4)
        """
        current_state = chars.astype(np.uint8).copy()
        next_state = np.empty_like(current_state)

        m = m % char_encode_mod

        for index in range(len(d_mod_range)):
            a = d_mod_range[index]
            # print(a)
            # print(d_mod_range[: index + 1])

            n = len(current_state)
            x0 = current_state[0]

            if index % 2 == 0:
                # y1 = x1^m
                next_state[0] = np.uint8((x0**m) + np.sum(d_mod_range[: index + 1]))
            else:
                # y1 = x1 + a1 + a2 + ... a_index
                next_state[0] = np.uint8(x0 + np.sum(d_mod_range[: index + 1]))

            for i in range(1, n):
                if i % 2 == 0:
                    next_state[i] = np.uint8(
                        current_state[i] - next_state[0] * current_state[i - 1]
                    )
                else:
                    next_state[i] = np.uint8(current_state[i] - x0 * next_state[i - 1])

            current_state, next_state = next_state, current_state

        return current_state

    @staticmethod
    @njit
    def decode(
        chars: np.ndarray, char_encode_mod: int, d_mod_range: np.ndarray, m: int
    ) -> np.ndarray:
        """
        improved version
        * from assighment5 graph algorithm

         (x1 x2 x3)

         [y1 = x1^m + a1, y2 = *,y3 = *]

         (x1 = y1 + a1 + a2, x2 = *,x3 = *)

         [y1 = x1^m + a1 + a2 + a3]

         (x1 = y1 + a1 + a2 + a3 + a4)
        """
        current_state = chars.astype(np.uint8).copy()
        next_state = np.empty_like(current_state)

        m = m % char_encode_mod

        current_state = chars.astype(np.uint8).copy()
        next_state = np.empty_like(current_state)

        for index in range(len(d_mod_range) - 1, -1, -1):
            a = d_mod_range[index]
            n = len(current_state)
            y0 = current_state[0]

            if index % 2 == 0:
                # TODO: need to fix decode
                # Reverse of: y0 = (x0**m + SUM) % mod
                next_state[0] = np.uint8(
                    ((y0 ** (1 / m)) - np.sum(d_mod_range[: index + 1]))
                )
            else:
                # y1 = x1 + a1 + a2 + ... a_index
                next_state[0] = np.uint8(y0 - np.sum(d_mod_range[: index + 1]))

            x0 = next_state[0]

            for i in range(1, n):
                if i % 2 == 0:
                    next_state[i] = np.uint8(current_state[i] + y0 * next_state[i - 1])
                else:
                    next_state[i] = np.uint8(
                        current_state[i] + x0 * current_state[i - 1]
                    )

            current_state, next_state = next_state, current_state

        return current_state
