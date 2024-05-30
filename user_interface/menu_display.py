

def display_difficulty_options():
    """
    Display the difficulty level options.
    """
    difficulty_options = {
        "1": "Easy",
        "2": "Medium",
        "3": "Hard"
    }
    print_menu_options("Choose difficulty level:", difficulty_options)


def display_post_solve_options():
    """
    Display the post-solve options.
    """
    post_solve_options = {
        "1": "Play a new game",
        "2": "Return to main menu"
    }
    print_menu_options("Please Select an Option", post_solve_options)


def display_hint_options():
    """
    Display the hint options.
    """
    hint_options = {
        "1": "Random cell",
        "2": "Specific cell"
    }
    print_menu_options("Choose an option for hint:", hint_options)


def display_save_location_prompt():
    """
    Display the save location options.
    """
    save_location_options = {
        "1": "Default location (current directory)",
        "2": "Custom location"
    }
    print_menu_options("Choose the save location:", save_location_options)


def print_menu_options(menu_title, options):
    """
    Print the menu options.

    Args:
        menu_title (str): Title of the menu.
        options (dict): Dictionary of menu options.
    """
    print(menu_title)
    for key, value in options.items():
        print(f"{key}. {value}")
