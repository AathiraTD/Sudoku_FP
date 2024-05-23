def display_main_menu():
    """
    Display the main menu with options.
    """
    menu_options = [
        "1. Start New Game",
        "2. Upload Sudoku",
        "3. Load Saved Game",
        "4. Exit"
    ]
    print("Main Menu:")
    print_menu_options(menu_options)


def print_menu_options(options, index=0):
    """
    Recursively print each menu option.

    Args:
        options (list): List of menu options.
        index (int): Current index to print.
    """
    if index < len(options):
        print(options[index])
        print_menu_options(options, index + 1)


def display_invalid_input(message):
    """
    Display an invalid input message.

    Args:
        message (str): The message to display.
    """
    print(message)
    display_main_menu()  # Ensure Menu option is displayed again


def display_difficulty_options():
    """
    Display the difficulty level options.
    """
    options = [
        "Choose difficulty level:",
        "1. Easy",
        "2. Medium",
        "3. Hard"
    ]
    for option in options:
        print(option)


def display_post_solve_options():
    """
    Display the post-solve options.
    """
    options = [
        "Please Select an Option",
        "1. Play a new game",
        "2. Return to main menu"
    ]
    for option in options:
        print(option)


def display_hint_options():
    """
    Display the hint options.
    """
    options = [
        "Choose an option for hint:",
        "1. Random cell",
        "2. Specific cell"
    ]
    for option in options:
        print(option)


def display_move_prompt():
    """
    Display the prompt for entering user moves.
    """
    print("Enter your moves in the format 'A1=5, B2=3, C3=7'. To make a cell empty - 'A1=None' :")


def display_save_location_prompt():
    """
    Display the save location options.
    """
    options = [
        "Choose the save location:",
        "1. Default location (current directory)",
        "2. Custom location"
    ]
    for option in options:
        print(option)
