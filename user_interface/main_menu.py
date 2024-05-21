import os
import sys
from user_interface.user_input import get_menu_choice
from user_actions.start_new_game import start_new_game
from user_actions.upload_sudoku import upload_sudoku
from user_actions.load_saved_game import load_saved_game


def display_main_menu() -> None:
    """
    Function to display the main menu to the user.
    """
    print("Sudoku Main Menu")
    print("1. Start New Game")
    print("2. Upload Sudoku")
    print("3. Load Saved Game")
    print("4. Exit")


def handle_menu_choice(config: dict, choice: int) -> None:
    """
    Function to handle the user's menu choice.

    Args:
        config (dict): Configuration settings.
        choice (int): The user's menu choice.
    """
    clear_screen()
    if choice == 1:
        start_new_game(config)  # Start a new game
    elif choice == 2:
        upload_sudoku()  # Upload a Sudoku puzzle
    elif choice == 3:
        load_saved_game(config)  # Load a saved game
    elif choice == 4:
        print("Exiting the game...")  # Exit the game
        return
    menu_loop(config)  # Recursive call to display the menu again


def menu_loop(config: dict) -> None:
    """
    Function to display the menu and handle user choice using recursion.

    Args:
        config (dict): Configuration settings.
    """
    clear_screen()
    display_main_menu()  # Display the main menu
    choice = get_menu_choice()  # Get the user's menu choice
    handle_menu_choice(config, choice)  # Handle the user's menu choice


def clear_screen() -> None:
    """
    Function to clear the console screen.
    """
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For Mac and Linux
        os.system('clear')
    if sys.stdout.isatty():
        print("\033[H\033[J", end='')  # ANSI escape sequences for terminals
    else:
        print("\n" * 100)  # Fallback for IDEs like PyCharm
