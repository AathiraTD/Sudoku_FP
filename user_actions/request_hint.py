from typing import Tuple, Optional
from core_data.grid.grid import Grid, update_cell
from core_data.cell_state import CellState
from core_data.coordinate import Coordinate
from puzzle_handler.solve.sudoku_validation import is_valid, count_solutions
from user_interface.display.display_grid import display_grid
from utils.grid_utils import find_random_empty_cell, try_values_recursive, label_to_index


def get_hint_choice() -> str:
    """
    Prompt the user to choose between a random or specific cell for the hint.
    """
    print("Do you want a hint for a random cell or a specific cell? (random/specific):")
    return input("> ").strip().lower()


def get_specific_cell(grid_size: int) -> Tuple[int, int]:
    """
    Prompt the user to enter a specific cell coordinate and validate the input.
    """
    print("Enter the cell coordinate in the format 'ColumnLabel RowNumber' (e.g., 'A4'):")

    def get_valid_specific_cell() -> Tuple[int, int]:
        """
        Recursively prompt the user until a valid specific cell coordinate is provided.
        """
        user_input = input("> ").strip().upper()
        coord = label_to_index(user_input, grid_size)
        if coord:
            return coord
        print(
            "Invalid cell coordinate. Please enter the coordinate in the format 'ColumnLabel RowNumber' (e.g., 'A4').")
        return get_valid_specific_cell()  # Recursive call for invalid input

    return get_valid_specific_cell()


def generate_hint(grid: Grid, row: int, col: int) -> Optional[int]:
    """
    Generate a valid hint value for the given cell.
    """

    def hint_callback(num: int, context: Tuple[Grid, int, int]) -> Optional[int]:
        """
        Callback function to check if a number is a valid hint for the given cell.
        """
        grid, row, col = context
        if is_valid(grid, row, col, num, grid.grid_size):
            test_grid = update_cell(grid, Coordinate(row, col, grid.grid_size), num, CellState.HINT)
            if count_solutions(test_grid, grid.grid_size) == 1:
                return num  # Return the valid hint value
        return None

    return try_values_recursive(list(range(1, grid.grid_size + 1)), hint_callback, (grid, row, col))


def request_hint(grid: Grid) -> Grid:
    """
    Function to handle hint requests.
    """
    choice = get_hint_choice()  # Get user's hint choice
    if choice == 'specific':
        row, col = get_specific_cell(grid.grid_size)  # Get specific cell coordinate from the user
    else:
        cell = find_random_empty_cell(grid)  # Find a random empty cell
        if cell is None:
            print("No empty cells available for a hint.")
            return grid
        row, col = cell

    cell = grid[row, col]
    if cell.state == CellState.PRE_FILLED:
        print(f"The cell {chr(ord('A') + row)}{col + 1} is prefilled and cannot be modified.")
        return grid

    if cell.state == CellState.USER_FILLED:
        print(
            f"The cell {chr(ord('A') + row)}{col + 1} already has a value {cell.value.value}. Do you want to overwrite it? (Y/N)")
        if input("> ").strip().upper() != 'Y':
            return grid

    hint_value = generate_hint(grid, row, col)  # Generate the hint value
    if hint_value is None:
        print(f"No valid hint could be generated for the cell {chr(ord('A') + row)}{col + 1}.")
        return grid

    grid = update_cell(grid, Coordinate(row, col, grid.grid_size), hint_value, CellState.HINT)  # Apply the hint
    print(f"Hint applied for cell {chr(ord('A') + row)}{col + 1}. Value: {hint_value}.")
    display_grid(grid)  # Display the updated grid
    return grid
