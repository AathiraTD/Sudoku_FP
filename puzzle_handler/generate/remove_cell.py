from typing import Set, Dict, Callable
from core_data.grid.grid import Grid, update_cell
from core_data.coordinate import Coordinate
from core_data.cell_state import CellState

from puzzle_handler.solve.sudoku_validation import count_solutions


def memoize(func: Callable) -> Callable:
    cache = {}

    def memoized_func(*args):
        # Convert arguments to a hashable form
        serialized_args = tuple(map(str, args))
        if serialized_args in cache:
            return cache[serialized_args]
        result = func(*args)
        cache[serialized_args] = result
        return result

    return memoized_func


@memoize
def memoized_count_solutions(grid: Grid, grid_size: int) -> int:
    return count_solutions(grid, grid_size)


def serialize_grid(grid: Grid) -> tuple:
    """
    Serialize the grid state into a hashable tuple of tuples.
    """
    return tuple((coord.row_index, coord.col_index, cell.value.value) for coord, cell in grid.cells.items())


def remove_cells_recursive(coordinates_of_cells_to_remove: Set[Coordinate], grid: Grid, grid_size: int,
                           cache: Dict[str, int] = None) -> Grid:
    """
    Recursively remove cells from the grid to create the puzzle.

    Args:
        coordinates_of_cells_to_remove (Set[Coordinate]): The set of coordinates of cells to be removed.
        grid (Grid): The current state of the grid.
        grid_size (int): The size of the grid.
        cache (Dict[str, int], optional): A cache to store the number of solutions for evaluated grids.

    Returns:
        Grid: The updated grid after removing the cells.
    """
    if cache is None:
        cache = {}

    if not coordinates_of_cells_to_remove:
        return grid  # Base case: No more cells to remove

    # Extract a cell coordinate to remove
    coord = coordinates_of_cells_to_remove.pop()

    # Create a new grid with the selected cell removed
    grid_with_cell_removed = update_cell(grid, coord, None, CellState.EMPTY)

    # Serialize grid state for caching
    serialized_grid_state = serialize_grid(grid_with_cell_removed)

    # Check the cache for the number of solutions
    if serialized_grid_state in cache:
        solution_count = cache[serialized_grid_state]
    else:
        solution_count = memoized_count_solutions(grid_with_cell_removed, grid_size)
        cache[serialized_grid_state] = solution_count

    if solution_count == 1:
        # If the grid still has a unique solution, continue with recursion
        return remove_cells_recursive(coordinates_of_cells_to_remove, grid_with_cell_removed, grid_size, cache)
    else:
        # If removing the cell makes the puzzle non-unique, backtrack and try the next cell
        return remove_cells_recursive(coordinates_of_cells_to_remove, grid, grid_size, cache)


def generate_coordinates_to_remove(grid_size: int, num: int) -> Set[Coordinate]:
    import random
    coords = set()

    def generate(n: int, coords: Set[Coordinate]) -> Set[Coordinate]:
        if n == 0:
            return coords
        row, col = random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)
        coord = Coordinate(row, col, grid_size)
        if coord not in coords:
            coords.add(coord)
            return generate(n - 1, coords)
        else:
            return generate(n, coords)

    return generate(num, coords)


def start_remove_cells(grid: Grid, grid_size: int, num_cells_to_remove: int) -> Grid:
    """
    Start the process of removing cells from the grid to create the puzzle.

    Args:
        grid (Grid): The initial state of the grid.
        grid_size (int): The size of the grid.
        num_cells_to_remove (int): The number of cells to remove.

    Returns:
        Grid: The generated Sudoku puzzle with cells removed.
    """
    coordinates_to_remove = generate_coordinates_to_remove(grid_size, num_cells_to_remove)
    return remove_cells_recursive(coordinates_to_remove, grid, grid_size)
