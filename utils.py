import matplotlib.pyplot as plt


def plot_grid(grid: list[list[int]]) -> None:
    """
    Plot the 2d-grid with placed figures and saves it as png file.
    """
    plt.imshow(grid)
    plt.gca().invert_yaxis()
    plt.savefig('polyomino_packing.png')


def print_grid(grid: list[list[int]]) -> None:
    """
    Print 2d grid to the console.
    """

    for line in reversed(grid):
        print(line, end='\n')


def init_distances(height: int, width: int) -> list:
    """
    Fill in the distance matrix with the appropriate values.
    """
    # radii = list()
    places = list()
    for i in range(1, height):
        # coordinates = list()
        for j in range(i + 1):
            if i < width:
                # coordinates.append([j, i])
                places.append([j, i])

        for j in range(i, 0, -1):
            if j <= width:
                # coordinates.append([i, j - 1])
                places.append([i, j - 1])

        # radii.append(coordinates)

    # radii.insert(0, [[0, 0]])
    places.insert(0, [0, 0])

    return places


def are_coords_free(figure_coords: list, grid_coords: list) -> True:
    """
    Check the passed coordinates that they exist and are free.
    """
    for coord in figure_coords:
        if coord not in grid_coords:
            return False
    return True


def count_cost(figure_coords: list) -> int:
    """
    Count the cost of the possible figure position.
    """
    cost = 0

    for coord in figure_coords:
        cost += coord[0] + coord[1]

    return cost


def place_figure_to_grid(figure_coords: list, grid: list[list[int]], figure_num: int) -> list:
    """
    Change the value of the corresponding coordinates to the figure number.
    """
    for coord in figure_coords:
        grid[coord[0]][coord[1]] = figure_num
    return grid


def find_best_place(places: list[tuple[list, int]]) -> tuple[list, int]:
    """
    Find the first minimal cost value and return the coordinates.
    """
    min_sum = float('inf')
    best_place = list()
    for index, place in enumerate(places):
        if place[1] < min_sum:
            min_sum = place[1]
            best_place = place
    return best_place


def exclude_coordinates_from_radii(figure_coordinates: list[list[int]], radii: list) -> list:
    """
    Remove occupied coordinates from the list of possible ones.
    """
    for coord in figure_coordinates:
        for num, radius in enumerate(radii):
            try:
                radius.remove(coord)
                if len(radius) == 0:
                    radii.pop(num)
            except ValueError:
                ...
    return radii
