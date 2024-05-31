import logging
from typing import Tuple, Optional, List, Callable, Any

from puzzle_handler.puzzle_solver.sudoku_solver import is_valid

# Import the compiled Cython function
from core_data.cell import Cell
from core_data.cell_state import CellState
from core_data.cell_value import CellValue
from core_data.coordinate import Coordinate
from core_data.grid import Grid
from core_data.row import Row
from utils.grid_utils import find_empty_cell


# def is_valid_sudoku(grid: Grid, row: int, col: int, num: int) -> bool:
#     grid_size = grid.grid_size
#     subgrid_size = int(grid_size ** 0.5)
# 
#     def in_row(r: int) -> bool:
#         return any(grid[r, c].value.value == num for c in range(grid_size))
# 
#     def in_col(c: int) -> bool:
#         return any(grid[r, c].value.value == num for r in range(grid_size))
# 
#     def in_subgrid(start_row: int, start_col: int) -> bool:
#         return any(
#             grid[r, c].value.value == num
#             for r in range(start_row, start_row + subgrid_size)
#             for c in range(start_col, start_col + subgrid_size)
#         )
# 
#     start_row, start_col = (row // subgrid_size) * subgrid_size, (col // subgrid_size) * subgrid_size
#     return not in_row(row) and not in_col(col) and not in_subgrid(start_row, start_col)

def get_possible_values(grid: Grid, row: int, col: int) -> set:
    grid_size = grid.grid_size
    subgrid_size = int(grid_size ** 0.5)
    possible_values = set(range(1, grid.grid_size + 1))

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


def find_empty_cell_with_fewest_options(grid: Grid) -> Optional[Tuple[int, int]]:
    min_options = float('inf')
    best_cell = None

    def find_best_cell(row: int, col: int, min_options: int, best_cell: Optional[Tuple[int, int]]) -> Optional[
        Tuple[int, int]]:
        if row >= grid.grid_size:
            return best_cell
        if col >= grid.grid_size:
            return find_best_cell(row + 1, 0, min_options, best_cell)

        cell = grid[row, col]
        if cell.value.value is None or cell.value.value == 0:  # Check for empty cells
            options = len(get_possible_values(grid, row, col))
            # print(f"Cell ({row}, {col}) has {options} options")  # Debug print
            if options < min_options:
                min_options = options
                best_cell = (row, col)
                # print(f"Best cell updated to ({row}, {col}) with {options} options")  # Debug print

        return find_best_cell(row, col + 1, min_options, best_cell)

    result = find_best_cell(0, 0, min_options, best_cell)
    # print(f"Best empty cell found: {result}")  # Debug print
    return result


def backtrack(grid: Grid) -> Tuple[Grid, bool]:
    logging.debug("Starting backtrack")

    grid = apply_naked_singles(grid)

    empty_cell = find_empty_cell_with_fewest_options(grid)
    if not empty_cell:
        logging.debug("No empty cells found, puzzle solved")
        return grid, True

    row, col = empty_cell
    logging.debug(f"Empty cell found at {row, col}")

    random_values = list(range(1, grid.grid_size + 1))
    sorted_values = sort_values_by_constraints(grid, row, col, random_values)

    def try_values_recursive(values: List[int], callback: Callable[[int, Any], Optional[Any]], context: Any) -> \
    Optional[Any]:
        if not values:
            return None

        result = callback(values[0], context)
        if result:
            return result

        return try_values_recursive(values[1:], callback, context)

    def backtrack_callback(value: int, context: Tuple[Grid, int, int]) -> Optional[Tuple[Grid, bool]]:
        grid, row, col = context
        numpy_grid = grid.to_numpy()  # Convert Grid to numpy array
        if is_valid(numpy_grid, row, col, value, grid.grid_size):
            new_grid = grid.with_updated_cell(Coordinate(row, col, grid.grid_size),
                                              Cell(CellValue(value, grid.grid_size), CellState.PRE_FILLED))
            solved_grid, success = backtrack(new_grid)
            if success:
                return solved_grid, True
        return None

    result = try_values_recursive(sorted_values, backtrack_callback, (grid, row, col))
    return result if result else (grid, False)


def apply_naked_singles(grid: Grid) -> Grid:
    grid_size = grid.grid_size

    def apply_to_cell(row: int, col: int, grid: Grid) -> Grid:
        if row >= grid_size:
            return grid

        if col >= grid_size:
            return apply_to_cell(row + 1, 0, grid)

        cell = grid[row, col]
        if cell and cell.value.value == 0:
            possible_values = get_possible_values(grid, row, col)
            if len(possible_values) == 1:
                new_value = possible_values.pop()
                coord = Coordinate(row, col, grid_size)
                grid = grid.with_updated_cell(coord, Cell(CellValue(new_value, grid_size), CellState.USER_FILLED))

        return apply_to_cell(row, col + 1, grid)

    return apply_to_cell(0, 0, grid)


def sort_values_by_constraints(grid: Grid, row: int, col: int, values: List[int]) -> List[int]:
    def sort_recursive(values: List[int], sorted_values: List[int]) -> List[int]:
        if not values:
            return sorted_values

        min_value = min(values, key=lambda val: count_constraints(grid, row, col, val))
        sorted_values.append(min_value)
        values.remove(min_value)
        return sort_recursive(values, sorted_values)

    return sort_recursive(values, [])


def count_constraints(grid: Grid, row: int, col: int, value: int) -> int:
    def count_in_row(r: int, col_idx: int, count: int) -> int:
        if col_idx >= grid.grid_size:
            return count
        if grid[r, col_idx].value.value == 0 and value in get_possible_values(grid, r, col_idx):
            count += 1
        return count_in_row(r, col_idx + 1, count)

    def count_in_col(c: int, row_idx: int, count: int) -> int:
        if row_idx >= grid.grid_size:
            return count
        if grid[row_idx, c].value.value == 0 and value in get_possible_values(grid, row_idx, c):
            count += 1
        return count_in_col(c, row_idx + 1, count)

    def count_in_subgrid(sr: int, sc: int, r: int, c: int, count: int) -> int:
        subgrid_size = int(grid.grid_size ** 0.5)
        if r >= sr + subgrid_size:
            return count
        if c >= sc + subgrid_size:
            return count_in_subgrid(sr, sc, r + 1, sc, count)
        if grid[r, c].value.value == 0 and value in get_possible_values(grid, r, c):
            count += 1
        return count_in_subgrid(sr, sc, r, c + 1, count)

    subgrid_size = int(grid.grid_size ** 0.5)
    start_row, start_col = (row // subgrid_size) * subgrid_size, (col // subgrid_size) * subgrid_size

    count = 0
    count = count_in_row(row, 0, count)
    count = count_in_col(col, 0, count)
    count = count_in_subgrid(start_row, start_col, start_row, start_col, count)

    return count


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
            # numpy_grid = grid.to_numpy()  # Convert Grid to numpy array
            if is_valid_sudoku(grid, row, col, num):
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


What
happpned?

What
I
did?

What
are
doing
for current scenario
