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


def get_places(height: int, width: int) -> list:
    """
    Fill in the distance matrix with the appropriate values.
    """
    places = list()
    for i in range(1, height):
        for j in range(i + 1):
            if i < width:
                places.append([j, i])

        for j in range(i, 0, -1):
            if j <= width:
                places.append([i, j - 1])

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


def exclude_coordinates(figure_coordinates, places):
    for coord in figure_coordinates:
        try:
            places.remove(coord)
        except ValueError:
            ...
    return places

