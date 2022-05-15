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


def init_distances(grid: list[list[int]]) -> tuple[list, list]:
    """
    Fill in the distance matrix with the appropriate values.
    """
    coordinates = list()
    coordinates.append([0, 0])
    for i in range(1, len(grid)):
        for j in range(i + 1):
            if i < len(grid[0]):
                grid[j][i] = i
                coordinates.append([j, i])

        for j in range(i, 0, -1):
            if j <= len(grid[0]):
                grid[i][j - 1] = i
                coordinates.append([i, j - 1])

    return grid, coordinates


def are_coords_free(figure_coords: list, grid: list[list[int]]) -> True:
    """
    Check the passed coordinates that they exist and are free.
    """
    for coord in figure_coords:
        if coord[0] < 0 or coord[1] < 0:
            return False
        try:
            if grid[coord[0]][coord[1]] != 0:
                return False
        except IndexError:
            return False
    return True


def count_cost(figure_coords: list, grid: list[list[int]]) -> int:
    """
    Count the cost of the possible figure position.
    """
    cost = 0
    for coord in figure_coords:
        cost += coord[0] + coord[1] + grid[coord[0]][coord[1]]

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


def exclude_coordinates(figure_coordinates: list[list[int]], arcs: list[int]) -> list[int]:
    """
    Remove occupied coordinates from the list of possible ones.
    """
    for coord in figure_coordinates:
        arcs.remove(coord)
    return arcs
