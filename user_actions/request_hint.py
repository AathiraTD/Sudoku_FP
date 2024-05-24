from typing import Optional, Tuple

from core_data.cell_state import CellState
from core_data.coordinate import Coordinate
from core_data.game_state import GameState
from core_data.grid.grid import Grid
from puzzle_handler.solve.puzzle_solver import count_solutions, is_valid, update_grid
from puzzle_handler.solve.sudoku_validation import has_empty_cells, \
    check_and_handle_completion
from user_interface.display.display_grid import display_grid
from user_interface.user_input_handler import get_hint_choice
from utils.grid_utils import find_random_empty_cell, try_values_recursive, label_to_index


def get_specific_cell(grid_size: int) -> Tuple[int, int]:
    """
    Prompt the user to enter a specific cell coordinate and validate the input.
    Returns a tuple of (row, col) representing the cell coordinate.
    """
    prompt = "Enter the cell coordinate in the format 'ColumnLabel RowNumber' (e.g., 'A4') or Back to return:\n> "
    user_input = input(prompt).strip().upper()
    coord = label_to_index(user_input, grid_size)
    if coord:
        return coord
    print("Invalid cell coordinate. Please enter the coordinate in the format 'ColumnLabel RowNumber' (e.g., 'A4').")
    return get_specific_cell(grid_size)  # Recursive call for invalid input


def generate_hint(grid: Grid, row: int, col: int) -> Optional[int]:
    """
    Generate a valid hint value for the given cell.
    """

    def hint_callback(num: int, context: Tuple[Grid, int, int]) -> Optional[int]:
        """
        Callback function to check if a number is a valid hint for the given cell.
        """
        grid, row, col = context
        if is_valid(grid, row, col, num):
            test_grid = update_grid(grid, Coordinate(row, col, grid.grid_size), num, CellState.HINT)
            if count_solutions(test_grid, grid.grid_size) == 1:
                return num  # Return the valid hint value
        return None

    context = (grid, row, col)
    return try_values_recursive(list(range(1, grid.grid_size + 1)), hint_callback, context)


def request_hint(game_state: GameState) -> GameState:
    """
    Request a hint for the given grid based on the user's choice and configuration.
    Returns the updated game state with the applied hint (if any).
    """
    hint_limit = game_state.config['hint_limit']

    if not game_state.can_use_hint():
        print("Hint limit reached. No more hints available.")
        return game_state

    choice = get_hint_choice()  # Get user's hint choice
    choice = validate_hint_choice(choice)  # Validate user input recursively

    if choice == 'specific':
        row, col = get_specific_cell(game_state.grid.grid_size)  # Get specific cell coordinate from the user
    else:
        cell = find_random_empty_cell(game_state.grid)  # Find a random empty cell
        if cell is None:
            print("No empty cells available for a hint.")
            return game_state
        row, col = cell

    cell = game_state.grid[row, col]
    if cell.state == CellState.PRE_FILLED:
        print(f"The cell {chr(ord('A') + row)}{col + 1} is prefilled and cannot be modified.")
        return game_state

    if cell.state == CellState.USER_FILLED:
        print(
            f"The cell {chr(ord('A') + row)}{col + 1} already has a value {cell.value.value}. Do you want to "
            f"overwrite it? (Y/N)")
        if input("> ").strip().upper() != 'Y':
            return game_state

    try:
        hint_value = generate_hint(game_state.grid, row, col)  # Generate the hint value
        if hint_value is None:
            print(f"No valid hint could be generated for the cell {chr(ord('A') + row)}{col + 1}.")
            return game_state

        new_grid = update_grid(game_state.grid, Coordinate(row, col, game_state.grid.grid_size), hint_value,
                               CellState.HINT)  # Apply the hint
        game_state = game_state.increment_hints().with_grid(new_grid)
        print(f"Hint applied for cell {chr(ord('A') + row)}{col + 1}. Value: {hint_value}.")
        print(f"Hints remaining: {game_state.hints_remaining()}")

        if not has_empty_cells(new_grid):  # Check for empty cells before triggering completion check
            game_state = check_and_handle_completion(game_state)

    except ValueError as e:
        print(f"System failed to generate hint. Please check your previous moves. Error: {e}")

    display_grid(game_state.grid)  # Display the updated grid
    return game_state


def validate_hint_choice(choice: str) -> str:
    """
    Validate the user's hint choice, re-prompting if necessary.
    """
    if choice not in ['random', 'specific']:
        print("Invalid choice. Please enter 'random' or 'specific'.")
        return validate_hint_choice(get_hint_choice())
    return choice
