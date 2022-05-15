import argparse

from polyomino import *
from utils import *

parser = argparse.ArgumentParser(description='Packing polyomino in a grid')
parser.add_argument('-grid_size', nargs=2, type=int)
parser.add_argument('-l_polyomino', type=int, nargs='+',
                    action='append', help='Each L-polyomino described with triple of numbers:'
                                          'length, ledge and number of instances')
parser.add_argument('-r_polyomino', type=int, nargs='+',
                    action='append', help='Each rectangular polyomino described with triple of numbers:'
                                          'width, height and number of instances')
args = parser.parse_args()

HEIGHT = args.grid_size[0]
WIDTH = args.grid_size[1]
NUM_OF_ROTATIONS = 4

grid_occupation = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]


def pack_polyomino(polyomino_list: list[Polyomino], grid: list, radii: list, show_grid: bool = False) -> bool:
    for num, polyomino in enumerate(polyomino_list):
        possibles_places = list()
        for rotation_num in range(NUM_OF_ROTATIONS):
            for coord in radii:
                polyomino.place_figure(0, 0)
                polyomino.rotate(rotation_num)
                polyomino.move_figure(coord[0], coord[1])
                if are_coords_free(polyomino.coordinates, grid):
                    possibles_places.append(
                        (polyomino.coordinates, count_cost(polyomino.coordinates)))

        if len(possibles_places) != 0:
            place = find_best_place(possibles_places)
            grid = place_figure_to_grid(place[0], grid, num + 1)
            exclude_coordinates(place[0], radii)
        else:
            return False

        if show_grid:
            print('---' * 3)
            print(f'Figure {num + 1}: {polyomino}')
            print_grid(grid)

    return True


if __name__ == "__main__":

    pol_list = list()
    common_area = 0

    if args.l_polyomino is not None:
        for l_polyomino in args.l_polyomino:
            for _ in range(l_polyomino[2]):
                polyomino = LPolyomino(size=(l_polyomino[0], l_polyomino[1]))
                pol_list.append(polyomino)
                common_area += polyomino.area

    if args.r_polyomino is not None:
        for r_polyomino in args.r_polyomino:
            for _ in range(r_polyomino[2]):
                polyomino = RPolyomino(size=(r_polyomino[0], r_polyomino[1]))
                pol_list.append(polyomino)
                common_area += polyomino.area

    print(f'A list of polyomino is given: {pol_list}')
    radii = init_distances(HEIGHT, WIDTH)
    pol_list.sort(key=lambda x: (x.perimeter, x.area), reverse=True)

    print(radii)

    if len(pol_list) == 0:
        print('Polyomino can NOT be packed to the grid: the list of figures is empty')
    elif common_area <= HEIGHT * WIDTH:
        if pack_polyomino(pol_list, grid_occupation, show_grid=False, radii=radii):
            print('SUCCESS: Polyomino can be packed to the grid.')
            plot_grid(grid_occupation)
        else:
            print('Polyomino can NOT be packed to the grid.')
    else:
        print('Polyomino can NOT be packed to the grid: common area of figures > size of grid')
