from core_data.grid.grid import Grid
from typing import Set
import math


def get_subgrid_possible_values(grid: Grid, row: int, col: int, possible_values: Set[int]) -> Set[int]:
    """
    Retrieve the possible values for a cell based on its subgrid.

    Args:
        grid (Grid): The Sudoku grid.
        row (int): The row index of the cell.
        col (int): The column index of the cell.
        possible_values (Set[int]): The set of possible values to be updated.

    Returns:
        Set[int]: The updated set of possible values for the cell.
    """
    grid_size = grid.grid_size  # Get the size of the grid
    subgrid_size = int(math.sqrt(grid_size))  # Calculate the size of the subgrid
    start_row, start_col = (row // subgrid_size) * subgrid_size, (
                col // subgrid_size) * subgrid_size  # Determine the starting indices of the subgrid

    def check_subgrid(r: int, c: int, possible_values: Set[int]) -> Set[int]:
        """
        Recursively update the possible values based on the current subgrid.

        Args:
            r (int): The current row index in the subgrid.
            c (int): The current column index in the subgrid.
            possible_values (Set[int]): The set of possible values to be updated.

        Returns:
            Set[int]: The updated set of possible values after considering the current subgrid.
        """
        if r >= start_row + subgrid_size:
            return possible_values  # Base case: All rows in the subgrid checked

        if c >= start_col + subgrid_size:
            return check_subgrid(r + 1, start_col, possible_values)  # Move to the next row in the subgrid

        cell = grid[r, c]  # Get the cell at the current row and column in the subgrid
        if cell and cell.value.value:
            possible_values.discard(cell.value.value)  # Remove the value from possible values

        return check_subgrid(r, c + 1, possible_values)  # Recursively check the next cell in the subgrid

    return check_subgrid(start_row, start_col,
                         possible_values)  # Start the recursion from the starting indices of the subgrid
