# helpers.py
from typing import Dict, Tuple
from core_data.cell_state import CellState
from core_data.coordinate import Coordinate
from core_data.grid.grid import Grid, update_cell
import math
from utils.grid_utils import find_empty_cell

# Custom cache dictionary
count_solutions_cache: Dict[Tuple, int] = {}

def grid_to_tuple(grid: Grid) -> Tuple:
    """
    Convert the grid to a tuple representation that can be used as a cache key.
    """
    return tuple((coord.row_index, coord.col_index, cell.value.value) for coord, cell in sorted(grid.cells.items()))

def is_valid(grid: Grid, row: int, col: int, num: int, grid_size: int) -> bool:
    """
    Check if placing a number in a specific cell follows Sudoku rules.
    """
    subgrid_size = int(math.sqrt(grid_size))

    def in_row(r: int) -> bool:
        return any(grid.cells[Coordinate(r, c, grid_size)].value.value == num for c in range(grid_size))

    def in_col(c: int) -> bool:
        return any(grid.cells[Coordinate(r, c, grid_size)].value.value == num for r in range(grid_size))

    def in_subgrid(start_row: int, start_col: int) -> bool:
        return any(
            grid.cells[Coordinate(r, c, grid_size)].value.value == num
            for r in range(start_row, start_row + subgrid_size)
            for c in range(start_col, start_col + subgrid_size)
        )

    start_row, start_col = (row // subgrid_size) * subgrid_size, (col // subgrid_size) * subgrid_size
    return not in_row(row) and not in_col(col) and not in_subgrid(start_row, start_col)

def count_solutions(grid: Grid, grid_size: int, max_solutions: int = 2) -> int:
    """
    Count the number of valid solutions for the Sudoku grid.
    """
    grid_tuple = grid_to_tuple(grid)
    if grid_tuple in count_solutions_cache:
        return count_solutions_cache[grid_tuple]

    empty_cell = find_empty_cell(grid)
    if not empty_cell:
        return 1

    row, col = empty_cell
    num_solutions = 0

    def count_values(num: int) -> int:
        nonlocal num_solutions
        if num > grid_size:
            return num_solutions
        if is_valid(grid, row, col, num, grid_size):
            new_grid = update_cell(grid, Coordinate(row, col, grid_size), num, CellState.PRE_FILLED)
            num_solutions += count_solutions(new_grid, grid_size, max_solutions)
            if num_solutions >= max_solutions:
                return num_solutions
        return count_values(num + 1)

    num_solutions = count_values(1)
    count_solutions_cache[grid_tuple] = num_solutions
    return num_solutions
