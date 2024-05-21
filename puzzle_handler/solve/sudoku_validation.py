from typing import Optional, Tuple, List, Dict
from functools import lru_cache
from core_data.cell import Cell
from core_data.cell_state import CellState
from core_data.grid.grid import Grid, update_cell
from core_data.coordinate import Coordinate
import math
from utils.grid_utils import find_empty_cell

# Custom cache dictionary
count_solutions_cache: Dict[Tuple, int] = {}

def grid_to_tuple(grid: Grid) -> Tuple:
    """
    Convert the grid to a tuple representation that can be used as a cache key.

    Args:
        grid (Grid): The Sudoku grid.

    Returns:
        Tuple: The tuple representation of the grid.
    """
    return tuple((coord.row_index, coord.col_index, cell.value.value) for coord, cell in sorted(grid.cells.items()))

def is_valid(grid: Grid, row: int, col: int, num: int, grid_size: int) -> bool:
    """
    Check if placing a number in a specific cell follows Sudoku rules.

    Args:
        grid (Grid): The current Sudoku grid.
        row (int): The row index.
        col (int): The column index.
        num (int): The number to place.
        grid_size (int): The size of the grid.

    Returns:
        bool: True if the move is valid, False otherwise.
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

    Args:
        grid (Grid): The current Sudoku grid.
        grid_size (int): The size of the grid.
        max_solutions (int): The maximum number of solutions to find.

    Returns:
        int: The number of valid solutions found.
    """
    # Convert grid to a tuple representation for caching
    grid_tuple = grid_to_tuple(grid)
    if grid_tuple in count_solutions_cache:
        return count_solutions_cache[grid_tuple]

    empty_cell = find_empty_cell(grid)
    if not empty_cell:
        return 1  # Base case: No empty cell found

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

def validate_move(grid: Grid, move: Tuple[Coordinate, Cell]) -> Tuple[bool, str]:
    """
    Validate a single user move.

    Args:
        grid (Grid): The Sudoku grid.
        move (Tuple[Coordinate, Cell]): A tuple containing the coordinate and the cell to be validated.

    Returns:
        Tuple[bool, str]: A tuple with a boolean indicating validity and a message.
    """
    coord, cell = move
    row, col = coord.row_index, coord.col_index
    value = cell.value.value

    if not (1 <= value <= grid.grid_size):
        return False, f"Invalid value: {value}. Must be between 1 and {grid.grid_size}."
    if not is_valid(grid, row, col, value, grid.grid_size):
        return False, f"Invalid move at {chr(ord('A') + row)}{col + 1}. Does not satisfy Sudoku rules."
    return True, f"Move {chr(ord('A') + row)}{col + 1}={value} applied successfully."

def is_puzzle_complete(grid: Grid) -> bool:
    """
    Check if the Sudoku puzzle is complete and valid.

    Args:
        grid (Grid): The Sudoku grid.

    Returns:
        bool: True if the puzzle is complete and valid, False otherwise.
    """
    def check_cell(row: int, col: int) -> bool:
        if row >= grid.grid_size:
            return True
        if col >= grid.grid_size:
            return check_cell(row + 1, 0)
        cell = grid.cells[Coordinate(row, col, grid.grid_size)]
        if cell.value.value is None or not is_valid(grid, row, col, cell.value.value, grid.grid_size):
            return False
        return check_cell(row, col + 1)

    return check_cell(0, 0)
