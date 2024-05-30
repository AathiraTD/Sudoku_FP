import logging
import random
from typing import Dict, List, Optional, Tuple, Callable, Any

from core_data.cell import Cell
from core_data.cell_state import CellState
from core_data.cell_value import CellValue
from core_data.coordinate import Coordinate
from core_data.grid import Grid
from core_data.row import Row
from utils.grid_utils import find_empty_cell

# Custom cache dictionary to store the results of counted solutions
count_solutions_cache: Dict[str, int] = {}


def grid_to_string(grid: Grid) -> str:
    """
    Convert the grid to a string representation that can be used as a cache key.

    Args:
        grid (Grid): The Sudoku grid.

    Returns:
        str: The string representation of the grid.
    """
    return ','.join(f"{coord.row_index},{coord.col_index},{cell.value.value}" for row in grid.rows for coord, cell in
                    row.cells.items())


def is_valid(grid: Grid, row: int, col: int, num: int) -> bool:
    """
    Check if placing a number in a cell is valid.

    Args:
        grid (Grid): The Sudoku grid.
        row (int): The row index.
        col (int): The column index.
        num (int): The number to place in the cell.

    Returns:
        bool: True if the number can be placed, False otherwise.
    """
    grid_size = grid.grid_size
    subgrid_size = int(grid_size ** 0.5)

    def in_row(r: int) -> bool:
        return any(grid[r, c].value.value == num for c in range(grid_size))

    def in_col(c: int) -> bool:
        return any(grid[r, c].value.value == num for r in range(grid_size))

    def in_subgrid(start_row: int, start_col: int) -> bool:
        return any(
            grid[r, c].value.value == num
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
    grid_size = grid.grid_size

    def apply_to_cell(row: int, col: int, grid: Grid) -> Grid:
        if row >= grid_size:
            return grid  # Base case: No more rows to process

        if col >= grid_size:
            return apply_to_cell(row + 1, 0, grid)  # Move to the next row if column index exceeds grid size

        cell = grid[row, col]
        if cell and cell.value.value == 0:
            possible_values = get_possible_values(grid, row, col)
            if len(possible_values) == 1:
                new_value = possible_values.pop()
                coord = Coordinate(row, col, grid_size)
                grid = update_grid(grid, coord, new_value, CellState.USER_FILLED)

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

    def remove_used_values(values: set, r: int, c: int) -> set:
        value = grid[r, c].value.value
        if value:
            values.discard(value)
        return values

    def process_column(idx: int, values: set) -> set:
        if idx >= grid_size:
            return values
        return process_column(idx + 1, remove_used_values(values, row, idx))

    def process_row(idx: int, values: set) -> set:
        if idx >= grid_size:
            return values
        return process_row(idx + 1, remove_used_values(values, idx, col))

    possible_values = process_column(0, possible_values)
    possible_values = process_row(0, possible_values)

    def process_subgrid(r: int, c: int, values: set) -> set:
        if r >= start_row + subgrid_size:
            return values
        if c >= start_col + subgrid_size:
            return process_subgrid(r + 1, start_col, values)
        return process_subgrid(r, c + 1, remove_used_values(values, r, c))

    start_row, start_col = (row // subgrid_size) * subgrid_size, (col // subgrid_size) * subgrid_size
    possible_values = process_subgrid(start_row, start_col, possible_values)

    return possible_values


def backtrack(grid: Grid) -> Tuple[Grid, bool]:
    logging.debug("Starting backtrack")
    empty_cell = find_empty_cell(grid)
    if not empty_cell:
        logging.debug("No empty cells found, puzzle solved")
        return grid, True  # Base case: No empty cell found, puzzle solved

    row, col = empty_cell
    logging.debug(f"Empty cell found at {row}, {col}")

    random_values = list(range(1, grid.grid_size + 1))
    random.shuffle(random_values)

    def backtrack_callback(value: int, context: Tuple[Grid, int, int]) -> Optional[Tuple[Grid, bool]]:
        grid, row, col = context
        if is_valid(grid, row, col, value):
            new_grid = update_grid(grid, Coordinate(row, col, grid.grid_size), value, CellState.PRE_FILLED)
            solved_grid, success = backtrack(new_grid)
            if success:
                return solved_grid, True  # Solution found
        return None

    result = try_values_recursive(random_values, backtrack_callback, (grid, row, col))
    if not result:
        pass
    return result if result else (grid, False)


def try_values_recursive(values: List[int], callback: Callable[[int, Any], Optional[Any]], context: Any) -> Optional[
    Any]:
    if not values:
        return None  # Base case: No values left to try

    result = callback(values[0], context)  # Apply the callback function to the current value
    if result:
        return result  # Return the result if the callback is successful

    return try_values_recursive(values[1:], callback, context)  # Recursive call to try the next value


def check_unique_solvability(grid: Grid) -> bool:
    """
    Check if the Sudoku grid has a unique solution.

    Args:
        grid (Grid): The Sudoku grid.

    Returns:
        bool: True if the grid has a unique solution, False otherwise.
    """
    return count_solutions(grid, grid.grid_size) == 1


def count_solutions(grid: Grid, grid_size: int, max_solutions: int = 2) -> int:
    """
    Count the number of valid solutions for the Sudoku grid.

    Args:
        grid (Grid): The Sudoku grid.
        grid_size (int): The size of the grid.
        max_solutions (int): The maximum number of solutions to count.

    Returns:
        int: The number of valid solutions found.
    """
    try:
        empty_cell = find_empty_cell(grid)
        if not empty_cell:
            return 1  # Base case: no empty cells means the puzzle is solved

        row, col = empty_cell
        num_solutions = 0

        def count_values(num: int) -> int:
            nonlocal num_solutions
            if num > grid_size:
                return num_solutions
            if is_valid(grid, row, col, num):
                new_grid = update_grid(grid, Coordinate(row, col, grid_size), num, CellState.PRE_FILLED)
                num_solutions += count_solutions(new_grid, grid_size, max_solutions)
                if num_solutions >= max_solutions:
                    return num_solutions
            return count_values(num + 1)

        num_solutions = count_values(1)
        return num_solutions
    except Exception as e:
        logging.error(f"Error in count_solutions: {e}")
        return 0


def update_grid(grid: Grid, coordinate: Coordinate, value: Optional[int], state: CellState) -> object:
    new_cells = {coord: cell for row in grid.rows for coord, cell in row.cells.items()}
    new_cells[coordinate] = Cell(CellValue(value, grid.grid_size), state)
    rows = tuple(
        Row({coord: new_cells[coord] for coord in new_cells if coord.row_index == row_index}, row_index) for row_index
        in range(grid.grid_size))
    return Grid(rows=rows, grid_size=grid.grid_size)


def upload_sudoku(grid: Grid) -> str:
    """
    Upload the Sudoku puzzle to an external solver or database.

    Args:
        grid (Grid): The Sudoku grid.

    Returns:
        str: The response from the solver or database.
    """
    # Placeholder function: replace with actual implementation
    return "Uploaded Sudoku grid successfully"
