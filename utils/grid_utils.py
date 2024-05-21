import random
from typing import Optional, Tuple, Set, Dict, List, Callable, Any
from core_data.grid.grid import Grid
from core_data.coordinate import Coordinate
from core_data.cell import Cell

def find_empty_cell(grid: Grid) -> Optional[Tuple[int, int]]:
    """
    Find the next empty cell in the Sudoku grid.

    Args:
        grid (Grid): The Sudoku grid.

    Returns:
        Optional[Tuple[int, int]]: The coordinates of the empty cell or None if no empty cells are found.
    """
    def find_cell(row: int, col: int) -> Optional[Tuple[int, int]]:
        if row >= grid.grid_size:
            return None  # Base case: No more rows

        if col >= grid.grid_size:
            return find_cell(row + 1, 0)  # Move to the next row if col exceeds size

        cell = grid[row, col]
        if cell.value.value is None or cell.value.value == 0:
            return row, col  # Empty cell found

        return find_cell(row, col + 1)  # Recursively check the next cell

    return find_cell(0, 0)


def find_random_empty_cell(grid: Grid) -> Optional[Tuple[int, int]]:
    """
    Find a random empty cell in the grid.

    Args:
        grid (Grid): The Sudoku grid.

    Returns:
        Optional[Tuple[int, int]]: The coordinates of an empty cell, or None if no empty cells are found.
    """
    empty_cells = [(coord.row_index, coord.col_index) for coord, cell in grid.cells.items() if cell.value.value is None]
    return random.choice(empty_cells) if empty_cells else None  # Randomly select an empty cell if available


def remove_cells(grid_size: int, num_cells_to_remove: int) -> Set[Tuple[int, int]]:
    """
    Recursively select cells to remove while ensuring balance across rows, columns, and subgrids.

    Args:
        grid_size (int): The size of the grid.
        num_cells_to_remove (int): The number of cells to remove.

    Returns:
        Set[Tuple[int, int]]: A set of coordinates for cells to be removed.
    """
    subgrid_size = int(grid_size ** 0.5)

    def select_cells(selected_cells: Set[Tuple[int, int]], remaining: int) -> Set[Tuple[int, int]]:
        if remaining == 0:
            return selected_cells  # Base case: no more cells to remove

        row, col = random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)
        subgrid_row, subgrid_col = row // subgrid_size, col // subgrid_size

        if (row, col) in selected_cells:
            return select_cells(selected_cells, remaining)  # Recurse if the cell is already selected

        # Check if selecting this cell would unbalance any row, column, or subgrid
        row_cells = {c for r, c in selected_cells if r == row}
        col_cells = {r for r, c in selected_cells if c == col}
        subgrid_cells = {(r, c) for r, c in selected_cells if r // subgrid_size == subgrid_row and c // subgrid_size == subgrid_col}

        if len(row_cells) >= grid_size - 1 or len(col_cells) >= grid_size - 1 or len(subgrid_cells) >= subgrid_size * subgrid_size - 1:
            return select_cells(selected_cells, remaining)  # Recurse if the selection would unbalance

        # Select the cell for removal and recurse
        return select_cells(selected_cells | {(row, col)}, remaining - 1)

    return select_cells(set(), num_cells_to_remove)


def try_values_recursive(values: List[int], callback: Callable[[int, Any], Optional[Any]], context: Any) -> Optional[Any]:
    """
    A generic recursive function to try values and apply a callback function.

    Args:
        values (List[int]): The list of values to try.
        callback (Callable[[int, Any], Optional[Any]]): The callback function to apply for each value.
        context (Any): Additional context or state information needed by the callback function.

    Returns:
        Optional[Any]: The result of the callback function, if any value is successful; otherwise, None.
    """
    if not values:
        return None  # Base case: No values left to try

    result = callback(values[0], context)  # Apply the callback function to the current value
    if result:
        return result  # Return the result if the callback is successful

    return try_values_recursive(values[1:], callback, context)  # Recursive call to try the next value


def label_to_index(label: str, grid_size: int) -> Optional[Tuple[int, int]]:
    """
    Convert a cell label (e.g., 'A1') to a grid index (row, col).

    Args:
        label (str): The cell label to convert.
        grid_size (int): The size of the grid.

    Returns:
        Optional[Tuple[int, int]]: A tuple representing the row and column index, or None if invalid.
    """
    # Validate the length and content of the label
    if len(label) < 2 or not label[0].isalpha() or not label[1:].isdigit():
        return None  # Return None if the format is invalid

    row = ord(label[0].upper()) - ord('A')  # Convert letter to row index
    col = int(label[1:]) - 1  # Convert number to column index

    # Check if the row and column are within the valid range
    if row < 0 or col < 0 or row >= grid_size or col >= grid_size:
        return None  # Return None if the index is out of bounds

    return row, col  # Return the valid row and column index