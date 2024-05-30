from user_interface.game_actions import get_game_actions
from user_interface.menu_options import get_menu_options


def display_main_menu() -> None:
    """
    Display the main menu with options.
    """
    menu_options = get_menu_options()  # Get the menu options dictionary
    print("Main Menu:")  # Print the main menu header
    display_menu_options_recursively(menu_options, 1)  # Display the menu options recursively


def display_menu_options_recursively(menu_options: dict, current_index: int) -> None:
    """
    Recursively display the menu options.

    Args:
        menu_options (dict): The menu options dictionary.
        current_index (int): The current index to display.
    """
    if current_index > len(menu_options):  # Base case: if the current index exceeds the menu length, return
        return

    if current_index in menu_options:  # Check if the current index exists in the menu options
        description, _ = menu_options[current_index]  # Get the description of the current menu option
        print(f"{current_index}. {description}")  # Print the current menu option

    display_menu_options_recursively(menu_options, current_index + 1)  # Recursive call to display the next menu option


def display_game_actions(actions: dict) -> None:
    """
    Display the game actions with options.

    Args:
        actions (dict): The game actions dictionary.
    """
    print("Choose a Game Action:")  # Print the game actions header
    game_action_options = get_game_actions()  # Get the game actions dictionary
    display_game_actions_recursively(game_action_options, 1)  # Display the game actions recursively


def display_game_actions_recursively(actions: dict, current_index: int) -> None:
    """
    Recursively display the game actions.

    Args:
        actions (dict): The game actions dictionary.
        current_index (int): The current index to display.
    """
    if current_index > len(actions):  # Base case: if the current index exceeds the actions length, return
        return

    if current_index in actions:  # Check if the current index exists in the actions
        description, _ = actions[current_index]  # Get the description of the current action
        print(f"{current_index}. {description}")  # Print the current action

    display_game_actions_recursively(actions, current_index + 1)  # Recursive call to display the next action


import os
import sys


def clear_screen() -> None:
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For Mac and Linux
        os.system('clear')
    if sys.stdout.isatty():
        print("\033[H\033[J", end='')  # ANSI escape sequences for terminals
    else:
        print("\n" * 100)  # Fallback for IDEs like PyCharm


def display_invalid_input(message):
    """
    Display an invalid input message.

    Args:
        message (str): The message to display.
    """
    print(message)
    # display_main_menu()  # Ensure Menu option is displayed again


def display_move_prompt():
    """
    Display the prompt for entering user moves.
    """
    print("Enter your moves in the format 'A1=5, B2=3, C3=7'. To make a cell empty - 'A1=None' :")
