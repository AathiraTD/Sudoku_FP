def get_main_menu_options() -> dict:
    """
    Return the main menu options.

    Returns:
        dict: The main menu options.
    """
    from user_actions.start_new_game import start_new_game
    from user_actions.upload_sudoku import upload_sudoku
    from user_actions.load_saved_game import load_saved_game
    return {
        1: ("Start New Game", start_new_game),
        2: ("Upload Sudoku", upload_sudoku),
        3: ("Load Saved Game", load_saved_game),
        4: ("Exit", None)  # None handler indicates exiting the game
    }


def get_difficulty_options() -> dict:
    """
    Return the difficulty level options.

    Returns:
        dict: The difficulty level options.
    """
    return {
        1: ("Easy", None),
        2: ("Medium", None),
        3: ("Hard", None)
    }


def get_post_solve_options() -> dict:
    """
    Return the post-solve options.

    Returns:
        dict: The post-solve options.
    """
    return {
        1: ("Play a new game", None),
        2: ("Return to main menu", None)
    }


def get_hint_options() -> dict:
    """
    Return the hint options.

    Returns:
        dict: The hint options.
    """
    return {
        1: ("Random cell", None),
        2: ("Specific cell", None)
    }


def get_save_location_options() -> dict:
    """
    Return the save location options.

    Returns:
        dict: The save location options.
    """
    return {
        1: ("Default location (current directory)", None),
        2: ("Custom location", None)
    }


def get_game_actions() -> dict:
    """
    Return the game actions.

    Returns:
        dict: The game actions.
    """
    from user_actions.make_a_move import make_a_move
    from user_actions.request_hint import request_hint
    from user_actions.save_game import save_game_to_file
    from user_actions.solve_puzzle import solve_puzzle
    from user_actions.undo_move import undo_move
    return {
        1: ("Make a move", make_a_move),
        2: ("Get a hint", request_hint),
        3: ("Undo last move", undo_move),
        4: ("Solve the puzzle", solve_puzzle),
        5: ("Save the game", lambda gs: (save_game_to_file(gs), gs)[1]),
        6: ("Back to main menu", None)
    }
