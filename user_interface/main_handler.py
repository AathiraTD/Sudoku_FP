import os
import sys

from user_actions.load_saved_game import load_saved_game
from user_actions.start_new_game import start_new_game
from user_actions.upload_sudoku import upload_sudoku
from user_interface.display.menu_display import display_main_menu
from user_interface.user_input_handler import get_menu_choice


def clear_screen() -> None:
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For Mac and Linux
        os.system('clear')
    if sys.stdout.isatty():
        print("\033[H\033[J", end='')  # ANSI escape sequences for terminals
    else:
        print("\n" * 100)  # Fallback for IDEs like PyCharm

def handle_menu_choice(config: dict, choice: int) -> bool:
    clear_screen()
    if choice == 1:
        start_new_game(config)  # Start a new game
    elif choice == 2:
        upload_sudoku(config)  # Upload a Sudoku puzzle
    elif choice == 3:
        load_saved_game(config)  # Load a saved game
    elif choice == 4:
        print("Exiting the game...")  # Exit the game
        return False
    return True

def menu_loop(config: dict) -> None:
    while True:
        clear_screen()
        display_main_menu()  # Display the main menu
        choice = get_menu_choice()  # Get the user's menu choice
        if not handle_menu_choice(config, choice):
            break  # Exit the loop if the user chooses to exit


if __name__ == "__main__":
    config = {"grid_size": 9, "hint_limit": 3}
    menu_loop(config)
