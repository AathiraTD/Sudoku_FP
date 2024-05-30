from user_interface.display.display_utilities import clear_screen
from user_interface.display.menu_display import display_invalid_input, display_menu_with_title
from user_interface.input.menu_enums import MainMenuOption, get_menu_options
from user_interface.input.user_input_handler import prompt_choice


def get_menu_choice(max_val: int) -> int:
    """
    Get the user's menu choice.

    Args:
        max_val (int): Maximum valid value.

    Returns:
        int: The user's menu choice.
    """
    return prompt_choice(1, max_val)


def handle_menu_choice(config: dict, choice: int, menu_options: dict) -> bool:
    """
    Handle the user's menu choice.

    Args:
        config (dict): Configuration settings.
        choice (int): The user's choice from the menu.
        menu_options (dict): Menu options with actions.

    Returns:
        bool: True to continue the menu loop, False to exit.
    """
    clear_screen()
    action = menu_options.get(choice)
    if action:
        _, handler = action
        if handler:
            handler(config)
            return True
        else:
            print("Exiting the game...")  # Exit the game
            return False
    display_invalid_input("Invalid choice. Please enter a valid number.")
    return True


def menu_loop(config: dict) -> None:
    """
    Main menu loop.

    Args:
        config (dict): Configuration settings.
    """
    menu_options = get_menu_options(MainMenuOption)  # Get menu options once

    def menu_loop_recursive():
        """
        Recursively handle the main menu loop.
        """
        clear_screen()
        display_menu_with_title("Main Menu", menu_options)  # Display the main menu
        menu_choice = get_menu_choice(len(menu_options))  # Get the user's menu choice
        if handle_menu_choice(config, menu_choice, menu_options):
            menu_loop_recursive()  # Continue the loop recursively

    menu_loop_recursive()  # Start the recursive loop
