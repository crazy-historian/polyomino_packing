from polyomino import *
from utils import *

HEIGHT = 7
WIDTH = 4
NUM_OF_ROTATION = 4


def pack_recursively(figures: list[Polyomino], places: list, grid: list) -> tuple[bool, list]:
    if len(figures) == 0:
        return True, grid

    for i, figure_i in enumerate(figures):
        for place in places:
            for rot_num in range(NUM_OF_ROTATION):
                figure_i.place_figure(0, 0)
                figure_i.rotate(rot_num)
                figure_i.move_figure(place[0], place[1])
                if are_coords_free(figure_coords=figure_i.coordinates, grid_coords=places):
                    grid = place_figure_to_grid(figure_coords=figure_i.coordinates, grid=grid,
                                                figure_num=figure_i.id_num)
                    if pack_recursively(figures=exclude_figure(figure_num=i, figures=figures.copy()),
                                        places=exclude_coordinates(figure_i.coordinates, places.copy()),
                                        grid=grid)[0] is True:
                        return True, grid
                    grid = place_figure_to_grid(figure_coords=figure_i.coordinates, grid=grid, figure_num=0)

    return False, grid


if __name__ == "__main__":
    figures = list()
    for i in range(1, 5):
        figures.append(LPolyomino(size=(4, 3), id_num=i))
    figures.sort(key=lambda x: (x.perimeter, x.area), reverse=True)

    grid_occupation = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
    places = init_distances(HEIGHT, WIDTH)

    if sum([figure.area for figure in figures]) > len(places):
        print('Polyomino can NOT be packed to the grid: common area of figures > size of grid')

    res, gr = pack_recursively(figures, places, grid_occupation)
    print(res)
    print_grid(gr)
    plot_grid(gr)
