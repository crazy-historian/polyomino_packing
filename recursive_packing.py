import time
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


def pack_recursively(
        figures: list[Polyomino],
        places: list, grid: list,
        pruning_rule: bool = False) -> tuple[bool, list]:
    if len(figures) == 0:
        return True, grid

    for i, figure_i in enumerate(figures):
        possible_places = find_possible_places(figure_i, places)
        possible_places.sort(key=lambda x: x[1])
        for pos_place in possible_places:
            grid = set_value_to_grid(figure_coords=pos_place[0], grid=grid,
                                     figure_num=figure_i.id_num)

            if pack_recursively(figures=figures[:i] + figures[i + 1:],
                                places=exclude_coordinates(pos_place[0], places.copy()),
                                grid=grid)[0] is True:
                return True, grid

            grid = set_value_to_grid(figure_coords=pos_place[0], grid=grid, figure_num=0)

        if pruning_rule is True:
            return False, grid

    return False, grid


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Packing polyomino in a grid')
    parser.add_argument('-grid_height', type=int)
    parser.add_argument('-grid_width', type=int)
    parser.add_argument('-pruning_rule', help='Boolean flag which defines '
                                              'the heuristic rule for pruning branches of a graph.',
                        action='store_true')
    parser.add_argument('-l_polyomino', type=int, nargs='+',
                        action='append', help='Each L-polyomino described with triple of numbers: '
                                              'length, ledge and number of instances')
    parser.add_argument('-r_polyomino', type=int, nargs='+',
                        action='append', help='Each rectangular polyomino described with triple of numbers: '
                                              'width, height and number of instances')
    args = parser.parse_args()

    HEIGHT = args.grid_height
    WIDTH = args.grid_width

    pruning = args.pruning_rule

    if pruning:
        print(f'Pruning is ENABLED')
    else:
        print(f'Pruning is DISABLED')
    print('---' * 5)

    grid_occupation = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
    grid_places = get_places(HEIGHT, WIDTH)

    polyomino_list = list()
    figure_num = 1
    print('A list of polyomino is given:')
    if args.l_polyomino is not None:
        for l_polyomino in args.l_polyomino:
            print(f'L-polyomino, size=({l_polyomino[0], l_polyomino[1]}, number of instances: {l_polyomino[2]})')
            for _ in range(l_polyomino[2]):
                polyomino = LPolyomino(id_num=figure_num, size=(l_polyomino[0], l_polyomino[1]))
                polyomino_list.append(polyomino)

                figure_num += 1

    if args.r_polyomino is not None:
        for r_polyomino in args.r_polyomino:
            print(f'R-polyomino, size=({r_polyomino[0], l_polyomino[1]}, number of instances: {r_polyomino[2]})')
            for _ in range(r_polyomino[2]):
                polyomino = RPolyomino(id_num=figure_num, size=(r_polyomino[0], r_polyomino[1]))
                polyomino_list.append(polyomino)
                figure_num += 1

    print(f'\nLength of the given list: {len(polyomino_list)}')

    print('---' * 5)
    common_area = sum([figure.area for figure in polyomino_list])
    if common_area > len(grid_places):
        print(
            f'Polyomino can NOT be packed to the grid:'
            f'common area of figures ({common_area}) > size of grid ({len(grid_places)})')
    elif len(polyomino_list) == 0:
        print('Polyomino can NOT be packed to the grid: list of figures')
    else:
        print(f'WIDTH = {WIDTH}, HEIGHT = {HEIGHT}')
        print(f'Common area: {common_area}')
        start = time.time()
        packing_exists, packing = pack_recursively(polyomino_list, grid_places, grid_occupation, pruning)
        if packing_exists is True:
            print('SUCCESS:  Polyomino can be packed to the grid')
            plot_grid(packing)
        else:
            print('FAIL: Polyomino can NOT be packed to the grid.')
        end = time.time()
        print('---' * 5)
        print(f'Elapsed time: {round(end - start, 3)}')
