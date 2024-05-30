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
