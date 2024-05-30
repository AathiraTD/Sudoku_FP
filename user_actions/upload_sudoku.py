import logging
from typing import Optional, List, Tuple

from core_data.cell import Cell
from core_data.cell_state import CellState
from core_data.cell_value import CellValue
from core_data.coordinate import Coordinate
from core_data.game_state import GameState
from core_data.grid import Grid
from puzzle_handler.puzzle_solver.puzzle_solver import apply_naked_singles
from user_interface.controller.game_actions_controller import game_actions
from user_interface.display.display_grid import display_grid
from user_interface.display.menu_display import display_menu_with_title
from user_interface.input.menu_enums import MainMenuOption, get_menu_options
from user_interface.input.user_input_handler import get_user_move
from utils.input_parsing import parse_user_input


def input_sudoku_values_recursively(grid: Grid, user_moves: List[Tuple[Coordinate, int]], index: int = 0) -> Optional[
    Grid]:
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
    cell_state = CellState.PRE_FILLED

    cell, error = Cell.create(cell_value, cell_state)
    if error is not None:
        print(f"Error: {error}")
        return None

    try:
        grid = update_grid(grid, coord, cell.value.value, cell.state)
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
        return False  # Ensure the function returns False for an invalid grid


def input_and_validate(config: dict, grid: Grid) -> Optional[Grid]:
    """
    Input values and validate the Sudoku grid.

    Args:
        config (dict): Configuration settings.
        grid (Grid): The Sudoku grid.

    Returns:
        Optional[Grid]: The updated grid if valid, otherwise None.
    """
    display_grid(grid)  # Display the current grid state

    print("Enter your moves in the format 'A1=5, B2=3, C3=7' or type 'menu' to return to the main menu:")
    user_input = get_user_move()  # Get user input moves

    if user_input.lower() == 'menu':
        display_menu_with_title("Main Menu", get_menu_options(MainMenuOption))  # Display the main menu
        return None

    try:
        user_moves = parse_user_input(user_input, grid.grid_size)
        if not user_moves:
            print("Error: Invalid input format. Please try again.")
            return input_and_validate(config, grid)  # Retry input and validation

        moves = [(Coordinate(coord[0], coord[1], grid.grid_size), value) for coord, value in user_moves]
        updated_grid = input_sudoku_values_recursively(grid, moves)  # Apply user input values

        if updated_grid is None:
            print("Failed to upload Sudoku. Please correct the errors and try again.")
            return input_and_validate(config, grid)  # Retry input and validation
        else:
            display_grid(updated_grid)  # Display the filled grid
            if validate_uploaded_grid(updated_grid):
                print("Uploaded Sudoku is valid and has a unique solution.")
                new_game_state = GameState(updated_grid, config, 0, [])
                game_actions(new_game_state)  # Proceed to game actions
                return updated_grid  # Return the valid updated grid
            else:
                print(
                    "Failed to upload Sudoku. The grid does not have a unique solution. Please correct the errors and "
                    "try again.")
                return input_and_validate(config, updated_grid)  # Retry input and validation
    except ValueError as e:
        print(f"Error: {e}")
        logging.error(f"ValueError: {e}")
        return input_and_validate(config, grid)  # Retry input and validation


def upload_sudoku(config: dict) -> None:
    """
    Upload a Sudoku puzzle and proceed to game actions if valid.

    Args:
        config (dict): Configuration settings.
    """
    grid_size = config.get('grid_size')  #
    if not grid_size or not isinstance(grid_size, int) or grid_size < 1:
        print("Error: Invalid grid size in the configuration.")
        return

    grid = Grid.create(grid_size)  # Use the Grid class to create an empty grid
    if grid is None:
        print("Error: Failed to create an empty grid.")
        return

    updated_grid = input_and_validate(config, grid)  # Input values and validate
    if updated_grid is not None:
        # Optionally do something with the updated grid if needed
        pass
