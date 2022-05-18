from polyomino import *
from utils import *

HEIGHT = 7
WIDTH = 4
NUM_OF_ROTATION = 4

grid_occupation = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
places = init_distances(HEIGHT, WIDTH)
# figures = [RPolyomino(id_num=1, size=(3, 2)),
#            LPolyomino(id_num=2, size=(4, 2)),
#            LPolyomino(id_num=3, size=(2, 2)),
#            LPolyomino(id_num=4, size=(2, 2)),
#            LPolyomino(id_num=5, size=(2, 2)),
#            LPolyomino(id_num=6, size=(2, 2)),
#            RPolyomino(id_num=7, size=(2, 1)),
#            LPolyomino(id_num=8, size=(4, 2)),]
figures = list()
for i in range(1, 9):
    figures.append(LPolyomino(size=(2, 2), id_num=i))
figures.sort(key=lambda x: (x.perimeter, x.area), reverse=True)

print_grid(grid_occupation)
print(places)
print(figures)


def exclude_coordinates(figure_coordinates, places):
    for coord in figure_coordinates:
        try:
            places.remove(coord)
        except ValueError:
            ...
    return places


def exclude_figure(figure_num, figures):
    if len(figures) != 0:
        figures.pop(figure_num)
    return figures


print('****' * 20)


def pack_recursively(figures: list[Polyomino], places: list, grid: list) -> tuple[bool, list]:
    if len(figures) == 0:
        return True, grid

    if sum([figure.area for figure in figures]) > len(places):
        return False, grid  ## exclude from recursive body

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


res, gr = pack_recursively(figures, places, grid_occupation)
print(res)
print_grid(gr)
plot_grid(gr)
