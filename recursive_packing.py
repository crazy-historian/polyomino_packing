import argparse

from polyomino import *
from utils import *

NUM_OF_ROTATION = 4


def find_possible_places(figure: Polyomino, places: list) -> list:
    possible_places = list()
    for place in places:
        for rot_num in range(NUM_OF_ROTATION):
            figure.place_figure(0, 0)
            figure.rotate(rot_num)
            figure.move_figure(place[0], place[1])
            if are_coords_free(figure_coords=figure.coordinates, grid_coords=places):
                possible_places.append((figure.coordinates, count_cost(figure.coordinates)))
    possible_places.sort(key=lambda x: x[1])
    return possible_places


def pack_recursively(figures: list[Polyomino], places: list, grid: list) -> tuple[bool, list]:
    if len(figures) == 0:
        return True, grid

    for i, figure_i in enumerate(figures):
        possible_places = find_possible_places(figure_i, places)
        possible_places.sort(key=lambda x: x[1])
        for pos_place in possible_places:
            grid = place_figure_to_grid(figure_coords=pos_place[0], grid=grid,
                                        figure_num=figure_i.id_num)

            if pack_recursively(figures=figures[:i] + figures[i + 1:],
                                places=exclude_coordinates(pos_place[0], places),
                                grid=grid)[0] is True:
                return True, grid

            grid = place_figure_to_grid(figure_coords=pos_place[0], grid=grid, figure_num=0)

    return False, grid


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Packing polyomino in a grid')
    parser.add_argument('-grid_height', type=int)
    parser.add_argument('-grid_width', type=int)
    parser.add_argument('-l_polyomino', type=int, nargs='+',
                        action='append', help='Each L-polyomino described with triple of numbers: '
                                              'length, ledge and number of instances')
    parser.add_argument('-r_polyomino', type=int, nargs='+',
                        action='append', help='Each rectangular polyomino described with triple of numbers: '
                                              'width, height and number of instances')
    args = parser.parse_args()

    HEIGHT = args.grid_height
    WIDTH = args.grid_width

    grid_occupation = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]

    polyomino_list = list()
    figure_num = 1
    if args.l_polyomino is not None:
        for l_polyomino in args.l_polyomino:
            for _ in range(l_polyomino[2]):
                polyomino = LPolyomino(id_num=figure_num, size=(l_polyomino[0], l_polyomino[1]))
                polyomino_list.append(polyomino)
                figure_num += 1

    if args.r_polyomino is not None:
        for r_polyomino in args.r_polyomino:
            for _ in range(r_polyomino[2]):
                polyomino = RPolyomino(id_num=figure_num, size=(r_polyomino[0], r_polyomino[1]))
                polyomino_list.append(polyomino)
                figure_num += 1

    polyomino_list.sort(key=lambda x: (x.perimeter, x.area), reverse=True)
    places = get_places(HEIGHT, WIDTH)

    print(f'A list of polyomino is given: {polyomino_list}')
    print(f'Length of the given list: {len(polyomino_list)}')

    if sum([figure.area for figure in polyomino_list]) > len(places):
        print('Polyomino can NOT be packed to the grid: common area of figures > size of grid')
    elif len(polyomino_list) == 0:
        print('Polyomino can NOT be packed to the grid: list of figures')
    else:
        packing_exists, packing = pack_recursively(polyomino_list, places, grid_occupation)
        if packing_exists is True:
            print('SUCCESS:  Polyomino can be packed to the grid')
            plot_grid(packing)
        else:
            print('Polyomino can NOT be packed to the grid.')
