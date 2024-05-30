from user_interface.display_manager import display_main_menu
from user_interface.display_utilities import clear_screen
from user_interface.menu_options import get_menu_options
from user_interface.user_input_handler import get_menu_choice


def handle_menu_choice(config: dict, choice: int, menu_options: dict) -> bool:
    """
    Handle the user's menu choice.

    Args:
        config (dict): Configuration settings.
        choice (str): The user's choice from the menu.
        menu_options (dict): Menu options with actions.

    Returns:
        bool: True to continue the menu loop, False to exit.
    """
    clear_screen()
    display_main_menu()
    action = menu_options.get(choice)
    if action:
        _, handler = action
        if handler:
            handler(config)
            return True
        else:
            print("Exiting the game...")  # Exit the game
            return False
    print("Invalid choice. Please enter a valid number.")
    return True


def menu_loop(config: dict) -> None:
    """
    Main menu loop.

    Args:
        config (dict): Configuration settings.
    """
    menu_options = get_menu_options()  # Get menu options once

    def menu_loop_recursive():
        clear_screen()
        display_main_menu()  # Display the main menu
        menu_choice = get_menu_choice()  # Get the user's menu choice
        if handle_menu_choice(config, menu_choice, menu_options):
            menu_loop_recursive()  # Continue the loop recursively

    menu_loop_recursive()  # Start the recursive loop
