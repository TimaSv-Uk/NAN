from abc import ABC, abstractmethod

import numpy as np


class BaseEncodeDecodeAlgorithm(ABC):
    @abstractmethod
    def encode(
        self,
    ) -> np.ndarray:
        raise NotImplementedError()

    @abstractmethod
    def decode(
        self,
    ) -> np.ndarray:
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def _find_neighbors(
    ) -> None:
        raise NotImplementedError()

    @abstractmethod
    @staticmethod
    def _reverse_find_neighbors(
    ) -> None:
        raise NotImplementedError()

