import numpy as np
from typing import Optional
from abc import ABC, abstractmethod


class Polyomino(ABC):
    """
    An abstract type of the polyomino which defines the necessary properties and methods
    """

    def __init__(self, size: tuple, id_num: Optional[int] = None):
        self.id_num = id_num
        self.size = size
        self.area = self._count_area()
        self.perimeter = self._count_perimeter()
        self.coordinates = list()

    def rotate(self, count: int) -> None:
        rot_matrix = np.array(((0, -1),
                               (1, 0)))

        for _ in range(count):
            for num, coord in enumerate(self.coordinates):
                point = np.array(coord)
                point = rot_matrix.dot(point)
                self.coordinates[num] = point.tolist()

    def move_figure(self, x: int, y: int) -> None:
        for num, _ in enumerate(self.coordinates):
            self.coordinates[num][0] += x
            self.coordinates[num][1] += y

    @abstractmethod
    def place_figure(self, x: int, y: int):
        ...

    @abstractmethod
    def _count_perimeter(self) -> int:
        ...

    @abstractmethod
    def _count_area(self) -> int:
        ...


class LPolyomino(Polyomino):
    """
    An implementation of Polyomino type for L-polyomino which looks like this:

    #
    # # -- (2, 2) L-polyomino

    #
    #
    # # -- (3, 2) L-polyomino

    """

    def __init__(self, size: tuple, id_num: Optional[int] = None):
        self.length = max(size)
        super().__init__(size, id_num)

    def _count_area(self):
        return self.size[0] + self.size[1] - 1

    def _count_perimeter(self) -> int:
        return (self.size[0] * 2 + 2) + (self.size[1] * 2 + 2) - 4

    def place_figure(self, x: int, y: int):
        self.coordinates = list()
        for i in range(self.size[0]):
            self.coordinates.append([x + i, y])

        for j in range(1, self.size[1]):
            self.coordinates.append([x, y + j])

    def __repr__(self):
        return f'LP {self.id_num}: size={self.size}'


class RPolyomino(Polyomino):
    """
     An implementation of Polyomino type for rectangular polyomino.
    """

    def __init__(self, size: tuple, id_num: Optional[int] = None):
        super().__init__(size, id_num)

    def _count_perimeter(self) -> int:
        return 2 * self.size[0] + 2 * self.size[1]

    def _count_area(self) -> int:
        return self.size[0] * self.size[1]

    def place_figure(self, x: int, y: int):
        self.coordinates = list()
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                self.coordinates.append([x + i, y + j])

    def __repr__(self):
        return f'RP {self.id_num}: size={self.size}'
