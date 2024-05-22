from core_data.grid.grid import Grid, update_cell
from core_data.coordinate import Coordinate
from core_data.cell_state import CellState
from puzzle_handler.solve.helpers import is_valid
from utils.grid_utils import find_empty_cell, try_values_recursive
from typing import Tuple, List, Callable, Any, Optional
import random


def backtrack(grid: Grid) -> Tuple[Grid, bool]:
    """
    Recursively apply the backtracking algorithm to solve the Sudoku grid.

    Args:
        grid (Grid): The Sudoku grid to solve.

    Returns:
        Tuple[Grid, bool]: The solved grid and a boolean indicating if the solution was found.
    """
    empty_cell = find_empty_cell(grid)
    if not empty_cell:
        return grid, True  # Base case: No empty cell found, puzzle solved

    row, col = empty_cell
    random_values = list(range(1, grid.grid_size + 1))
    random.shuffle(random_values)

    def backtrack_callback(value: int, context: Tuple[Grid, int, int]) -> Optional[Tuple[Grid, bool]]:
        """
        Callback function to check if a value is valid for the given cell during backtracking.
        """
        grid, row, col = context
        if is_valid(grid, row, col, value,grid.grid_size):
            new_grid = update_cell(grid, Coordinate(row, col, grid.grid_size), value, CellState.PRE_FILLED)
            solved_grid, success = backtrack(new_grid)
            if success:
                return solved_grid, True  # Solution found
        return None

    result = try_values_recursive(random_values, backtrack_callback, (grid, row, col))
    return result if result else (grid, False)


