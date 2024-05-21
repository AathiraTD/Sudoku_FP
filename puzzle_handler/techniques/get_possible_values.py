from core_data.grid.grid import Grid
from core_data.coordinate import Coordinate
from typing import Set
from puzzle_handler.techniques.get_column_possible_values import get_column_possible_values
from puzzle_handler.techniques.get_subgrid_possible_values import get_subgrid_possible_values


def get_possible_values(grid: Grid, row: int, col: int) -> Set[int]:
    """
    Retrieve the possible values for a cell based on its row, column, and subgrid.

    Args:
        grid (Grid): The Sudoku grid.
        row (int): The row index of the cell.
        col (int): The column index of the cell.

    Returns:
        Set[int]: A set of possible values for the cell.
    """
    grid_size = grid.grid_size  # Get the size of the grid
    possible_values = set(range(1, grid_size + 1))  # Initialize possible values with all potential numbers

    def get_row_possible_values(col_index: int, possible_values: Set[int]) -> Set[int]:
        """
        Recursively update the possible values based on the current row.

        Args:
            col_index (int): The current column index.
            possible_values (Set[int]): The set of possible values to be updated.

        Returns:
            Set[int]: The updated set of possible values after considering the current row.
        """
        if col_index >= grid_size:
            return possible_values  # Base case: All columns checked

        cell = grid[row, col_index]  # Get the cell at the current row and column
        if cell and cell.value.value:
            possible_values.discard(cell.value.value)  # Remove the value from possible values

        return get_row_possible_values(col_index + 1, possible_values)  # Recursively check the next column

    possible_values = get_row_possible_values(0, possible_values)  # Update possible values based on the row
    possible_values = get_column_possible_values(grid, row, col,
                                                 possible_values)  # Update possible values based on the column
    possible_values = get_subgrid_possible_values(grid, row, col,
                                                  possible_values)  # Update possible values based on the subgrid

    return possible_values
