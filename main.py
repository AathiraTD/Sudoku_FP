import sys
import traceback
import os
from user_interface.main_menu import display_main_menu
from user_interface.user_input import get_menu_choice
from user_actions.start_new_game import start_new_game
from user_actions.upload_sudoku import upload_sudoku
from user_actions.load_saved_game import load_saved_game
from config.config import load_config, get_config_path


def clear_screen():
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


def handle_menu_choice(config, choice):
    """
    Function to handle the user's menu choice.
    """
    clear_screen()
    if choice == 1:
        start_new_game(config)
    elif choice == 2:
        upload_sudoku()
    elif choice == 3:
        load_saved_game()
    elif choice == 4:
        print("Exiting the game...")
        return
    menu_loop(config)  # Recursive call to display the menu again


def menu_loop(config):
    """
    Function to display the menu and handle user choice using recursion.
    """
    clear_screen()
    display_main_menu()
    choice = get_menu_choice()
    handle_menu_choice(config, choice)


def main():
    """
    Main function to display the menu and start the game based on user choice.
    """
    try:
        # Load the configuration
        config_path = get_config_path()
        config = load_config(config_path)

        # Start the menu loop
        menu_loop(config)  # Initial call to start the menu loop

    except Exception as e:
        with open("error_log.txt", "w") as f:
            f.write(traceback.format_exc())
        input("An error occurred. Press Enter to exit...")  # Keeps the window open in case of an error


if __name__ == "__main__":
    main()
