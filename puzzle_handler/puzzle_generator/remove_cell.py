import logging
from typing import Set, Dict, Callable, Tuple

from core_data.cell_state import CellState
from core_data.coordinate import Coordinate
from core_data.grid import Grid, update_grid
from puzzle_handler.puzzle_solver.puzzle_solver import count_solutions


def memoize(func: Callable) -> Callable:
    cache = {}

    def memoized_func(*args):
        serialized_args = tuple(map(str, args))  # Convert arguments to a hashable form
        if serialized_args in cache:
            return cache[serialized_args]
        result = func(*args)
        cache[serialized_args] = result
        return result

    return memoized_func


@memoize
def memoized_count_solutions(grid: Grid, grid_size: int) -> int:
    return count_solutions(grid, grid_size)


def serialize_grid(grid: Grid) -> Tuple:
    try:
        # Serialize the grid state into a hashable tuple of tuples
        return tuple((coord.row_index, coord.col_index, cell.value.value) for row in grid.rows for coord, cell in
                     row.cells.items())
    except Exception as e:
        logging.error(f"Error in serialize_grid: {e}")
        return ()


def remove_cells_recursive(coordinates_of_cells_to_remove: Set[Coordinate], grid: Grid, grid_size: int,
                           cache: Dict[str, int] = None) -> Grid:
    try:
        # Initialize cache if not provided
        if cache is None:
            cache = {}

        # Base case: No more cells to remove
        if not coordinates_of_cells_to_remove:
            return grid

        # Extract a cell coordinate to remove
        coord = coordinates_of_cells_to_remove.pop()

        # Create a new grid with the selected cell removed
        grid_with_cell_removed = update_grid(grid, coord, None, CellState.EMPTY)

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

    except Exception as e:
        logging.error(f"Error in remove_cells_recursive: {e}")
        raise


def generate_coordinates_to_remove(grid_size: int, num: int) -> Set[Coordinate]:
    import random

    def generate(n: int, coords: Set[Coordinate]) -> Set[Coordinate]:
        if n == 0:
            return coords  # Base case: no more cells to puzzle_generator
        row, col = random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)
        coord = Coordinate(row, col, grid_size)
        if coord not in coords:
            return generate(n - 1, coords | {coord})  # Use set union to add new coordinate
        else:
            return generate(n, coords)

    return generate(num, set())


def start_remove_cells(grid: Grid, grid_size: int, num_cells_to_remove: int) -> Grid:
    try:
        # Generate coordinates of cells to remove
        coordinates_to_remove = generate_coordinates_to_remove(grid_size, num_cells_to_remove)
        # Start the recursive removal process
        return remove_cells_recursive(coordinates_to_remove, grid, grid_size)
    except Exception as e:
        logging.error(f"Error in start_remove_cells: {e}")
        raise
