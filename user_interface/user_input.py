import os
from typing import Tuple

from user_interface.display.menu_display import display_invalid_input, display_difficulty_options, display_move_prompt, \
    display_hint_options, display_save_location_prompt, display_post_solve_options


def get_menu_choice() -> int:
    """
    Get the user's menu choice from the main menu.

    Returns:
        int: The user's menu choice.
    """
    return prompt_choice(1, 4)


def prompt_choice(min_val: int, max_val: int) -> int:
    """
    Prompt the user to input a choice within a specified range.

    Args:
        min_val (int): Minimum valid choice.
        max_val (int): Maximum valid choice.

    Returns:
        int: The user's valid choice.
    """
    try:
        choice = int(input("> "))  # Get input from the user
        if min_val <= choice <= max_val:
            return choice  # Return valid choice
        else:
            display_invalid_input(f"Invalid choice. Please enter a number between {min_val} and {max_val}.")
            return prompt_choice(min_val, max_val)  # Recursive call for invalid input
    except ValueError:
        display_invalid_input(f"Invalid input. Please enter a number between {min_val} and {max_val}.")
        return prompt_choice(min_val, max_val)  # Recursive call for non-integer input


def get_difficulty_choice() -> str:
    """
    Get the user's choice of difficulty level.

    Returns:
        str: The user's difficulty choice ('easy', 'medium', 'hard').
    """
    display_difficulty_options()
    choice = prompt_choice(1, 3)
    return ["easy", "medium", "hard"][choice - 1]  # Return corresponding difficulty


def get_user_move() -> str:
    """
    Get the user's move input.

    Returns:
        str: The user's move input.
    """
    display_move_prompt()
    return prompt_user_move()  # Start the recursion


def prompt_user_move() -> str:
    """
    Recursively prompt the user for a valid move input.

    Returns:
        str: The user's valid move input.
    """
    user_input = input("> ").strip()  # Get input from the user

    # Split the input string into individual moves
    moves = user_input.split(",")

    # Check if each move is in the correct format
    for move in moves:
        move = move.strip()  # Remove leading/trailing whitespaces
        if not move:
            continue  # Skip empty strings

        if "=" not in move:  # Check if the move contains an '=' sign
            display_invalid_input(f"Invalid move format: '{move}'. Expected format: 'A1=5'.")
            return prompt_user_move()

        cell, value = move.split("=")  # Split the move into cell and value
        if not (len(cell) == 2 and cell[0].isalpha() and cell[
            1].isdigit()):  # Check if the cell is in the correct format
            display_invalid_input(f"Invalid cell format: '{cell}'. Expected format: 'A1'.")
            return prompt_user_move()

        if value.lower() != "none" and not value.isdigit():  # Check if the value is a digit or 'None'
            display_invalid_input(f"Invalid value: '{value}'. Expected a digit or 'None'.")
            return prompt_user_move()

    return user_input  # Return the valid user input


def get_post_solve_choice() -> int:
    """
    Get the user's post-solve choice.

    Returns:
        int: The user's valid choice (1 for new game, 2 for main menu).
    """
    display_post_solve_options()
    return prompt_choice(1, 2)


def get_hint_choice() -> str:
    """
    Get the user's choice for hint type.

    Returns:
        str: The user's choice ('random' or 'specific').
    """
    display_hint_options()
    choice = prompt_choice(1, 2)
    return 'random' if choice == 1 else 'specific'


def prompt_for_file_details() -> Tuple[str, str]:
    """
    Prompt the user for the file name and save location.

    Returns:
        Tuple[str, str]: The file name and the directory path.
    """
    # Prompt for file name
    file_name = input("Enter the file name (without extension): ").strip()
    if not file_name.endswith(".json"):
        file_name += ".json"

    display_save_location_prompt()
    location_choice = prompt_choice(1, 2)

    if location_choice == 1:
        return file_name, os.getcwd()  # Return the current directory
    elif location_choice == 2:
        directory = input("Enter the custom directory path: ").strip()
        if os.path.isdir(directory):
            return file_name, directory  # Return the custom directory if it exists
        else:
            display_invalid_input("Invalid directory. Saving to the default location instead.")
            return file_name, os.getcwd()  # Use the default directory if the custom one is invalid
