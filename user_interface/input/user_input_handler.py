# user_interface/input/user_input_handler.py

import os

from core_data.cell import Cell
from core_data.cell_state import CellState
from core_data.cell_value import CellValue
from puzzle_handler.solve.puzzle_solver import update_grid
from user_interface.display.menu_display import display_invalid_input, display_move_prompt, display_menu_with_title
from user_interface.input.menu_options import get_difficulty_options, get_post_solve_options, get_hint_options, \
    get_save_location_options


def get_menu_choice() -> int:
    """
    Get the user's menu choice.

    Returns:
        int: The user's menu choice.
    """
    return prompt_choice(1, 4)


def prompt_choice(min_val: int, max_val: int) -> int:
    """
    Prompt the user for a valid choice.

    Args:
        min_val (int): Minimum valid value.
        max_val (int): Maximum valid value.

    Returns:
        int: The user's choice.
    """
    choice = validate_choice(input("> "), min_val, max_val)
    if choice is None:
        display_invalid_input(f"Invalid input. Please enter a number between {min_val} and {max_val}.")
        return prompt_choice(min_val, max_val)
    return choice


def validate_choice(choice: str, min_val: int, max_val: int) -> int | None:
    """
    Validate the user's choice.

    Args:
        choice (str): The user's choice as a string.
        min_val (int): Minimum valid value.
        max_val (int): Maximum valid value.

    Returns:
        int: The validated choice, or None if invalid.
    """
    try:
        choice = int(choice)
        if min_val <= choice <= max_val:
            return choice
    except ValueError:
        pass
    return None


def get_difficulty_choice() -> str:
    """
    Get the user's choice of difficulty level.

    Returns:
        str: The chosen difficulty level.
    """
    display_menu_with_title("Choose difficulty level:", get_difficulty_options())
    choice = prompt_choice(1, 3)
    return ["easy", "medium", "hard"][choice - 1]


def get_user_move() -> str:
    """
    Get the user's move input.

    Returns:
        str: The user's move input.
    """
    display_move_prompt()
    return prompt_user_move()


def prompt_user_move() -> str:
    """
    Prompt the user for their move input.

    Returns:
        str: The user's move input.
    """
    user_input = input("> ").strip()
    if not validate_moves(user_input):
        return prompt_user_move()
    return user_input


def validate_moves(user_input: str) -> bool:
    """
    Validate the user's move input.

    Args:
        user_input (str): The user's move input as a string.

    Returns:
        bool: True if valid, False otherwise.
    """
    moves = user_input.split(",")
    for move in moves:
        move = move.strip()
        if not move:
            continue
        if "=" not in move:
            display_invalid_input(f"Invalid move format: '{move}'. Expected format: 'A1=5'.")
            return False
        cell, value = move.split("=")
        if not (len(cell) == 2 and cell[0].isalpha() and cell[1].isdigit()):
            display_invalid_input(f"Invalid cell format: '{cell}'. Expected format: 'A1'.")
            return False
        if value.lower() != "none" and not value.isdigit():
            display_invalid_input(f"Invalid value: '{value}'. Expected a digit or 'None'.")
            return False
    return True


def get_post_solve_choice() -> int:
    """
    Get the user's post-solve choice.

    Returns:
        int: The user's post-solve choice.
    """
    display_menu_with_title("Please Select an Option", get_post_solve_options())
    return prompt_choice(1, 2)


def get_hint_choice() -> str:
    """
    Get the user's hint choice.

    Returns:
        str: The user's hint choice.
    """
    display_menu_with_title("Choose an option for hint:", get_hint_options())
    choice = prompt_choice(1, 2)
    return 'random' if choice == 1 else 'specific'


def prompt_for_file_details() -> tuple:
    """
    Prompt the user for file name and directory details.

    Returns:
        tuple: The file name and directory.
    """
    file_name = input("Enter the file name (without extension): ").strip()
    if not file_name:
        return "", ""

    if not file_name.endswith(".json"):
        file_name += ".json"

    display_menu_with_title("Choose the save location:", get_save_location_options())
    location_choice = prompt_choice(1, 2)
    directory = get_directory_choice(location_choice)
    return file_name, directory


def get_directory_choice(location_choice: int) -> str:
    """
    Get the directory choice based on user input.

    Args:
        location_choice (int): The user's directory choice.

    Returns:
        str: The chosen directory path.
    """
    if location_choice == 1:
        return os.getcwd()
    elif location_choice == 2:
        directory = input("Enter the custom directory path: ").strip()
        if os.path.isdir(directory):
            return directory
        else:
            display_invalid_input("Invalid directory. Saving to the default location instead.")
            return os.getcwd()


def input_sudoku_values_recursively(grid, user_moves, index: int = 0):
    """
    Recursively input values into the Sudoku grid.

    Args:
        grid: The Sudoku grid.
        user_moves: The list of user moves.
        index: The current index of the move being processed.

    Returns:
        The updated Sudoku grid, or None if any move is invalid.
    """
    if index >= len(user_moves):
        return grid

    coord, value = user_moves[index]
    if not (1 <= value <= grid.grid_size):
        display_invalid_input(
            f"Error: Invalid value {value} for cell {coord}. Value must be between 1 and {grid.grid_size}.")
        return None

    cell_value = CellValue(value, grid.grid_size)
    cell_state = CellState.USER_FILLED

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
