import json
from typing import Optional, List, Tuple, Dict
from core_data.grid.grid import Grid, update_cell
from core_data.cell import Cell
from core_data.cell_state import CellState
from core_data.cell_value import CellValue
from core_data.coordinate import Coordinate
from user_interface.display.display_grid import display_grid
from user_interface.display.menu_display import display_main_menu
from user_interface.user_input import get_user_move
from user_interface.game_actions import game_actions
from utils.grid_utils import convert_user_moves, create_empty_grid
from puzzle_handler.solve.puzzle_solver import apply_naked_singles, count_solutions, check_unique_solvability


def input_sudoku_values_recursively(grid: Grid, user_moves: List[Tuple[Coordinate, int]], index: int = 0) -> Optional[Grid]:
    """
    Recursively input values into the Sudoku grid.

    Args:
        grid (Grid): The Sudoku grid.
        user_moves (List[Tuple[Coordinate, int]]): The list of user moves.
        index (int): The current index of the move being processed.

    Returns:
        Optional[Grid]: The updated Sudoku grid, or None if any move is invalid.
    """
    if index >= len(user_moves):
        return grid

    coord, value = user_moves[index]
    if not (1 <= value <= grid.grid_size):
        print(f"Error: Invalid value {value} for cell {coord}. Value must be between 1 and {grid.grid_size}.")
        return None

    cell_value = CellValue(value, grid.grid_size)
    cell_state = CellState.USER_FILLED

    cell, error = Cell.create(cell_value, cell_state)
    if error is not None:
        print(f"Error: {error}")
        return None

    try:
        grid = update_cell(grid, coord, cell.value.value, cell.state, skip_validation=False)
    except ValueError as e:
        print(f"Error: {e}")
        return None

    return input_sudoku_values_recursively(grid, user_moves, index + 1)


def validate_uploaded_grid(grid: Grid) -> bool:
    """
    Validate the uploaded Sudoku grid.

    Args:
        grid (Grid): The Sudoku grid to validate.

    Returns:
        bool: True if the grid is valid and has a unique solution, False otherwise.
    """
    # Apply naked singles technique
    grid = apply_naked_singles(grid)

    # Count solutions and check unique solvability
    if count_solutions(grid, grid.grid_size) == 1 and check_unique_solvability(grid):
        return True
    else:
        print("Error: The grid does not have a unique solution.")
        return False


def input_and_validate(config: dict, grid: Grid) -> None:
    """
    Input values and validate the Sudoku grid.

    Args:
        config (dict): Configuration settings.
        grid (Grid): The Sudoku grid.
    """
    display_grid(grid)  # Display the current grid state

    print("Enter your moves in the format 'A1=5, B2=3, C3=7' or type 'menu' to return to the main menu:")
    user_input = get_user_move()  # Get user input moves

    if user_input.lower() == 'menu':
        display_main_menu()  # Display the main menu
        return

    user_moves = convert_user_moves(user_input, grid.grid_size)
    if user_moves is None:
        print("Error: Invalid input format. Please try again.")
        input_and_validate(config, grid)  # Retry input and validation
        return

    updated_grid = input_sudoku_values_recursively(grid, user_moves)  # Apply user input values

    if updated_grid is None:
        print("Failed to upload Sudoku. Please correct the errors and try again.")
        input_and_validate(config, grid)  # Retry input and validation
    else:
        display_grid(updated_grid)  # Display the filled grid

        if validate_uploaded_grid(updated_grid):
            print("Uploaded Sudoku is valid and has a unique solution.")
            game_actions(config, updated_grid)  # Proceed to game actions
        else:
            print("Failed to upload Sudoku. Please correct the errors and try again.")
            input_and_validate(config, updated_grid)  # Retry input and validation


def upload_sudoku(config: dict) -> None:
    """
    Upload a Sudoku puzzle and proceed to game actions if valid.

    Args:
        config (dict): Configuration settings.
    """
    grid_size = config.get('grid_size')
    if not grid_size or not isinstance(grid_size, int) or grid_size < 1:
        print("Error: Invalid grid size in the configuration.")
        return

    grid = create_empty_grid(grid_size)  # Create an empty grid
    if grid is None:
        print("Error: Failed to create an empty grid.")
        return

    input_and_validate(config, grid)  # Input values and validate