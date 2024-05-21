from typing import Optional, Tuple

from core_data.cell import Cell
from core_data.cell_state import CellState
from core_data.grid.grid import Grid, update_cell
from core_data.coordinate import Coordinate
import math

from utils.grid_utils import find_empty_cell


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

    def in_row(r: int, c: int) -> bool:
        if c >= grid_size:
            return False  # Base case: No more columns
        if grid[r, c].value.value == num:
            return True  # Found the number in the row
        return in_row(r, c + 1)  # Recursively check the next column

    def in_col(r: int, c: int) -> bool:
        if r >= grid_size:
            return False  # Base case: No more rows
        if grid[r, c].value.value == num:
            return True  # Found the number in the column
        return in_col(r + 1, c)  # Recursively check the next row

    def in_subgrid(start_row: int, start_col: int, r: int, c: int) -> bool:
        if r >= start_row + subgrid_size:
            return False  # Base case: No more rows in subgrid
        if c >= start_col + subgrid_size:
            return in_subgrid(start_row, start_col, r + 1, start_col)  # Move to the next row in subgrid
        if grid[r, c].value.value == num:
            return True  # Found the number in the subgrid
        return in_subgrid(start_row, start_col, r, c + 1)  # Recursively check the next cell in subgrid

    start_row, start_col = (row // subgrid_size) * subgrid_size, (col // subgrid_size) * subgrid_size
    return not in_row(row, 0) and not in_col(0, col) and not in_subgrid(start_row, start_col, start_row, start_col)


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

    empty_cell = find_empty_cell(grid)
    if not empty_cell:
        return 1  # Base case: No empty cell found

    row, col = empty_cell
    num_solutions = 0

    def count_values(num: int) -> int:
        nonlocal num_solutions
        if num > grid_size:
            return num_solutions  # Base case: No more values to check
        if is_valid(grid, row, col, num, grid_size):
            new_grid = update_cell(grid, Coordinate(row, col, grid_size), num, CellState.PRE_FILLED)
            num_solutions += count_solutions(new_grid, grid_size, max_solutions)
            if num_solutions >= max_solutions:
                return num_solutions  # Stop if max solutions are found
        return count_values(num + 1)  # Recursively check the next value

    return count_values(1)


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
    for row in range(grid.grid_size):
        for col in range(grid.grid_size):
            cell = grid[row, col]
            if cell.value.value is None or not is_valid(grid, row, col, cell.value.value, grid.grid_size):
                return False
    return True
