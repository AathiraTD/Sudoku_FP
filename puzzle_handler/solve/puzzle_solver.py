from functools import reduce
from typing import List, Tuple, Dict
from core_data.grid.grid import Grid, update_cell
from core_data.coordinate import Coordinate
from core_data.cell_state import CellState
from core_data.cell_value import CellValue
from core_data.cell import Cell
from utils.grid_utils import find_empty_cell

# Custom cache dictionary
count_solutions_cache: Dict[str, int] = {}


def grid_to_tuple(grid: Grid) -> Tuple:
    """
    Convert the grid to a tuple representation that can be used as a cache key.

    Args:
        grid (Grid): The Sudoku grid.

    Returns:
        Tuple: The tuple representation of the grid.
    """
    return tuple((coord.row_index, coord.col_index, cell.value.value) for coord, cell in sorted(grid.cells.items()))


def is_valid(grid: Grid, row: int, col: int, num: int) -> bool:
    """
    Check if placing a number in a specific cell follows Sudoku rules.

    Args:
        grid (Grid): The current Sudoku grid.
        row (int): The row index.
        col (int): The column index.
        num (int): The number to place.

    Returns:
        bool: True if the move is valid, False otherwise.
    """
    grid_size = grid.grid_size
    subgrid_size = int(grid_size ** 0.5)

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


def apply_naked_singles(grid: Grid) -> Grid:
    """
    Apply the naked singles technique to the Sudoku grid.

    Args:
        grid (Grid): The Sudoku grid.

    Returns:
        Grid: The updated grid after applying the naked singles technique.
    """
    grid_size = grid.grid_size  # Get the size of the grid

    def apply_to_cell(row: int, col: int, grid: Grid) -> Grid:
        """
        Recursively apply the naked singles technique to each cell in the grid.

        Args:
            row (int): The current row index.
            col (int): The current column index.
            grid (Grid): The current state of the grid.

        Returns:
            Grid: The updated grid after applying the naked singles technique to the current cell.
        """
        if row >= grid_size:
            return grid  # Base case: No more rows to process

        if col >= grid_size:
            return apply_to_cell(row + 1, 0, grid)  # Move to the next row if column index exceeds grid size

        cell = grid.cells[Coordinate(row, col, grid_size)]  # Get the cell at the current row and column
        if cell and cell.value.value == 0:
            possible_values = get_possible_values(grid, row, col)  # Get possible values for the cell
            if len(possible_values) == 1:
                new_value = possible_values.pop()  # If only one possible value, set it
                coord = Coordinate(row, col, grid_size)  # Create a coordinate for the cell
                grid = update_cell(grid, coord, new_value, CellState.USER_FILLED)  # Update the cell in the grid

        return apply_to_cell(row, col + 1, grid)  # Recursively process the next cell

    return apply_to_cell(0, 0, grid)  # Start the recursion from the first cell


def get_possible_values(grid: Grid, row: int, col: int) -> set:
    """
    Get possible values for a cell in the Sudoku grid.

    Args:
        grid (Grid): The Sudoku grid.
        row (int): The row index.
        col (int): The column index.

    Returns:
        set: A set of possible values for the cell.
    """
    grid_size = grid.grid_size
    subgrid_size = int(grid_size ** 0.5)
    possible_values = set(range(1, grid_size + 1))

    def remove_used_values(used_values: set, r: int, c: int) -> set:
        value = grid.cells[Coordinate(r, c, grid_size)].value.value
        if value:
            used_values.discard(value)
        return used_values

    possible_values = reduce(
        lambda values, idx: remove_used_values(values, row, idx),
        range(grid_size),
        possible_values
    )
    possible_values = reduce(
        lambda values, idx: remove_used_values(values, idx, col),
        range(grid_size),
        possible_values
    )

    start_row, start_col = (row // subgrid_size) * subgrid_size, (col // subgrid_size) * subgrid_size
    for r in range(start_row, start_row + subgrid_size):
        for c in range(start_col, start_col + subgrid_size):
            value = grid.cells[Coordinate(r, c, grid_size)].value.value
            if value:
                possible_values.discard(value)

    return possible_values


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
        if is_valid(grid, row, col, num):
            new_grid = update_cell(grid, Coordinate(row, col, grid_size), num, CellState.PRE_FILLED)
            num_solutions += count_solutions(new_grid, grid_size, max_solutions)
            if num_solutions >= max_solutions:
                return num_solutions
        return count_values(num + 1)

    num_solutions = count_values(1)
    count_solutions_cache[grid_tuple] = num_solutions
    return num_solutions


def check_unique_solvability(grid: Grid) -> bool:
    """
    Check if the Sudoku grid has a unique solution.

    Args:
        grid (Grid): The Sudoku grid.

    Returns:
        bool: True if the grid has a unique solution, False otherwise.
    """
    return count_solutions(grid, grid.grid_size) == 1
