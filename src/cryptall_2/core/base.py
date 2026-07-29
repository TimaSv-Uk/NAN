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

    @abstractmethod
    def __find_neighbors(
        self,
    ) -> None:
        raise NotImplementedError()

    @abstractmethod
    def __reverse_find_neighbors(
        self,
    ) -> None:
        raise NotImplementedError()

