import os

from core_data.cell import Cell
from core_data.cell_state import CellState
from core_data.cell_value import CellValue
from core_data.grid import update_grid
from user_interface.display.menu_display import display_invalid_input, display_menu_with_title, display_move_prompt
from user_interface.input.menu_enums import DifficultyOption, PostSolveOption, HintOption, \
    SaveLocationOption, get_menu_options


def get_menu_choice(max_val: int) -> int:
    return prompt_choice(1, max_val)


def prompt_choice(min_val: int, max_val: int) -> int:
    choice = validate_choice(input("> "), min_val, max_val)
    if choice is None:
        display_invalid_input(f"Invalid input. Please enter a number between {min_val} and {max_val}.")
        return prompt_choice(min_val, max_val)
    return choice


def validate_choice(choice: str, min_val: int, max_val: int) -> int | None:
    try:
        choice = int(choice)
        if min_val <= choice <= max_val:
            return choice
    except ValueError:
        pass
    return None


def get_difficulty_choice() -> str:
    display_menu_with_title("Choose difficulty level:", get_menu_options(DifficultyOption))
    choice = prompt_choice(1, len(DifficultyOption))
    return ["easy", "medium", "hard"][choice - 1]


def get_user_move() -> str:
    display_move_prompt()
    return prompt_user_move()


def prompt_user_move() -> str:
    user_input = input("> ").strip()
    if not validate_moves(user_input):
        return prompt_user_move()
    return user_input


def validate_moves(user_input: str) -> bool:
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
    display_menu_with_title("Please Select an Option", get_menu_options(PostSolveOption))
    return prompt_choice(1, len(PostSolveOption))


def get_hint_choice() -> str:
    display_menu_with_title("Choose an option for hint:", get_menu_options(HintOption))
    choice = prompt_choice(1, len(HintOption))
    return 'random' if choice == 1 else 'specific'


def prompt_for_file_details() -> tuple:
    file_name = input("Enter the file name (without extension): ").strip()
    if not file_name:
        return "", ""

    if not file_name.endswith(".json"):
        file_name += ".json"

    display_menu_with_title("Choose the save location:", get_menu_options(SaveLocationOption))
    location_choice = prompt_choice(1, len(SaveLocationOption))
    directory = get_directory_choice(location_choice)
    return file_name, directory


def get_directory_choice(location_choice: int) -> str:
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
