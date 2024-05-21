from core_data.grid.grid import Grid
from typing import Set


def get_column_possible_values(grid: Grid, row: int, col: int, possible_values: Set[int]) -> Set[int]:
    """
    Retrieve the possible values for a cell based on its column.

    Args:
        grid (Grid): The Sudoku grid.
        row (int): The current row index to start checking from.
        col (int): The column index of the cell.
        possible_values (Set[int]): The set of possible values to be updated.

    Returns:
        Set[int]: The updated set of possible values for the cell.
    """
    grid_size = grid.grid_size  # Get the size of the grid

    def check_column(row_index: int, possible_values: Set[int]) -> Set[int]:
        """
        Recursively update the possible values based on the current column.

        Args:
            row_index (int): The current row index.
            possible_values (Set[int]): The set of possible values to be updated.

        Returns:
            Set[int]: The updated set of possible values after considering the current column.
        """
        if row_index >= grid_size:
            return possible_values  # Base case: All rows checked

        cell = grid[row_index, col]  # Get the cell at the current row and column
        if cell and cell.value.value:
            possible_values.discard(cell.value.value)  # Remove the value from possible values

        return check_column(row_index + 1, possible_values)  # Recursively check the next row

    return check_column(0, possible_values)  # Start the recursion from the first row
