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

def input_sudoku_values_recursively(grid: Grid, user_moves: List[Tuple[Coordinate, int]], index: int = 0) -> Grid:
    """
    Recursively input values into the Sudoku grid.

    Args:
        grid (Grid): The Sudoku grid.
        user_moves (List[Tuple[Coordinate, int]]): The list of user moves.
        index (int): The current index of the move being processed.

    Returns:
        Grid: The updated Sudoku grid.
    """
    if index >= len(user_moves):
        return grid

    coord, value = user_moves[index]
    cell = Cell(CellValue(value, grid.grid_size), CellState.USER_FILLED)
    grid = update_cell(grid, coord, cell.value.value, cell.state, skip_validation=True)

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
    grid = input_sudoku_values_recursively(grid, user_moves)  # Apply user input values
    display_grid(grid)  # Display the filled grid

    if validate_uploaded_grid(grid):
        print("Uploaded Sudoku is valid and has a unique solution.")
        game_actions(config, grid)  # Proceed to game actions
    else:
        print("Failed to upload Sudoku. Please correct the errors and try again.")
        input_and_validate(config, grid)  # Retry input and validation

def upload_sudoku(config: dict) -> None:
    """
    Upload a Sudoku puzzle and proceed to game actions if valid.

    Args:
        config (dict): Configuration settings.
    """
    grid = create_empty_grid()  # Create an empty grid
    input_and_validate(config, grid)  # Input values and validate
