import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from abc import ABC, abstractmethod

HEIGHT = 7
WIDTH = 4

NUM_OF_ROTATIONS = 4

grid_occupation = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
grid_distances = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]


# cmap = [
#     'Accent', 'Accent_r', 'Blues',
#     'Blues_r', 'BrBG', 'BrBG_r',
#     'BuGn', 'BuGn_r', 'BuPu', 'BuPu_r',
#     'CMRmap', 'CMRmap_r', 'Dark2', 'Dark2_r',
#     'GnBu', 'GnBu_r', 'Greens', 'Greens_r', 'Greys', 'Greys_r', 'OrRd', 'OrRd_r', 'Oranges', 'Oranges_r', 'PRGn', 'PRGn_r', 'Paired', 'Paired_r', 'Pastel1',
#            'Pastel1_r', 'Pastel2'
#         'Pastel2_r', 'PiYG', 'PiYG_r', 'PuBu', 'PuBuGn', 'PuBuGn_r', 'PuBu_r', 'PuOr', 'PuOr_r', 'PuRd', 'PuRd_r',
#     'Purples', 'Purples_r', 'RdBu', 'RdBu_r', 'RdGy', 'RdGy_r', 'RdPu', 'RdPu_r', 'RdYlBu', 'RdYlBu_r', 'RdYlGn',
#     'RdYlGn_r', 'Reds', 'Reds_r', 'Set1', 'Set1_r', 'Set2', 'Set2_r', 'Set3', 'Set3_r', 'Spectral', 'Spectral_r',
#     'Wistia', 'Wistia_r', 'YlGn', 'YlGnBu', 'YlGnBu_r', 'YlGn_r', 'YlOrBr', 'YlOrBr_r', 'YlOrRd', 'YlOrRd_r',
#     'afmhot', 'afmhot_r', 'autumn', 'autumn_r', 'binary', 'binary_r', 'bone', 'bone_r', 'brg', 'brg_r', 'bwr',
#     'bwr_r', 'cividis', 'cividis_r', 'cool', 'cool_r', 'coolwarm', 'coolwarm_r', 'copper', 'copper_r', 'cubehelix',
#     'cubehelix_r', 'flag', 'flag_r', 'gist_earth', 'gist_earth_r', 'gist_gray', 'gist_gray_r', 'gist_heat',
#     'gist_heat_r', 'gist_ncar', 'gist_ncar_r', 'gist_rainbow', 'gist_rainbow_r', 'gist_stern', 'gist_stern_r',
#     'gist_yarg', 'gist_yarg_r', 'gnuplot', 'gnuplot2', 'gnuplot2_r', 'gnuplot_r', 'gray', 'gray_r', 'hot', 'hot_r',
#     'hsv', 'hsv_r', 'inferno', 'inferno_r', 'jet', 'jet_r', 'magma',


def plot_grid(grid: list):
    plt.imshow(list(reversed(grid)))
    plt.show()


def print_grid(grid: list) -> None:
    for line in reversed(grid):
        print(line, end='\n')


def init_distances(grid: list) -> tuple[list, list]:
    coordinates = list()
    coordinates.append([0, 0])
    for i in range(1, HEIGHT):
        for j in range(i + 1):
            if i < WIDTH:
                grid[j][i] = i
                coordinates.append([j, i])

        for j in range(i, 0, -1):
            if j <= WIDTH:
                grid[i][j - 1] = i
                coordinates.append([i, j - 1])

    return grid, coordinates


def are_coords_free(figure_coords: list, grid: list) -> True:
    for coord in figure_coords:
        if coord[0] < 0 or coord[1] < 0:
            return False
        try:
            if grid[coord[0]][coord[1]] != 0:
                return False
        except IndexError:
            return False
    return True


def sum_distances(figure_coords: list, grid: list) -> int:
    sum = 0
    for coord in figure_coords:
        sum += coord[0] + coord[1] + grid[coord[0]][coord[1]]

    return sum


def place_figure_to_grid(figure_coords: list, grid: list, figure_num: int) -> list:
    for coord in figure_coords:
        grid[coord[0]][coord[1]] = figure_num
    return grid


def find_best_place(places: list[tuple[list, int]]):
    min_sum = float('inf')
    best_place = list()
    for index, place in enumerate(places):
        if place[1] < min_sum:
            min_sum = place[1]
            best_place = place
    return best_place


def exclude_coordinates(figure_coordinates, arcs):
    for coord in figure_coordinates:
        arcs.remove(coord)
    return arcs


class Polyomino(ABC):
    def __init__(self, size: tuple):
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
    def __init__(self, size: tuple):
        self.length = max(size)
        super().__init__(size)

    def _count_area(self):
        return self.size[0] + self.size[1] - 1

    def _count_perimeter(self) -> int:
        return 6 + 2 * (self.length - 2)

    def place_figure(self, x: int, y: int):
        self.coordinates = list()
        for i in range(self.length):
            self.coordinates.append([x, y + i])

        self.coordinates.append([x + 1, y])

    def __repr__(self):
        return f'LP: size={self.size}, area={self.area}, perimeter={self.perimeter}'


class RPolyomino(Polyomino):
    def __init__(self, size: tuple):
        super().__init__(size)

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
        return f'RP: size={self.size}, area={self.area}, perimeter={self.perimeter}'


def is_square(figure: Polyomino):
    return isinstance(figure, RPolyomino) and figure.size[0] == figure.size[1]


# polyomino_list = [RPolyomino(size=(2, 2)), LPolyomino(size=(3, 2)), LPolyomino(size=(2, 2)), LPolyomino(size=(2, 2))]
polyomino_list = [LPolyomino(size=(4, 2)), RPolyomino(size=(3, 2)),
                  LPolyomino(size=(3, 2)), LPolyomino(size=(2, 2)), RPolyomino(size=(1, 2)), LPolyomino(size=(2, 2)),
                  RPolyomino(size=(1, 3)), LPolyomino(size=(2, 2))]

polyomino_list.sort(key=lambda x: (x.perimeter, -x.area), reverse=True)
# print(polyomino_list)

grid_distances, arcs = init_distances(grid_distances)
# print_grid(grid_distances)
# print(coords)

example = LPolyomino(size=(3, 2))
example.place_figure(0, 2)
print(example.coordinates)
for num in range(1, NUM_OF_ROTATIONS):
    example.rotate(num)
    print(example.coordinates)


def pack_polyomino(polyomino_list: list[Polyomino], grid: list) -> bool:
    for num, polyomino in enumerate(polyomino_list):
        print('---' * 3)
        possibles_places = list()
        print(f'Figure {num + 1}: {polyomino}')
        for rotation_num in range(NUM_OF_ROTATIONS):
            for coord in arcs:  # todo: create generator
                polyomino.place_figure(0, 0)
                polyomino.rotate(rotation_num)
                polyomino.move_figure(coord[0], coord[1])
                # print(arcs)
                # print(f'rot num: {rotation_num}, coord - {coord}, pol coords: {polyomino.coordinates}')
                if are_coords_free(polyomino.coordinates, grid):
                    possibles_places.append(
                        (polyomino.coordinates, sum_distances(polyomino.coordinates, grid_distances)))

        if len(possibles_places) != 0:
            place = find_best_place(possibles_places)
            grid = place_figure_to_grid(place[0], grid, num + 1)
            # print(f'pos places {possibles_places}')
            # print(f'best place {place[0]}')
            exclude_coordinates(place[0], arcs)
        print_grid(grid)
    plot_grid(grid)
