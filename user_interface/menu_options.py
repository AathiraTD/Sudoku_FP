from user_actions.make_a_move import make_a_move
from user_actions.request_hint import request_hint
from user_actions.save_game import save_game_to_file
from user_actions.solve_puzzle import solve_puzzle
from user_actions.start_new_game import start_new_game
from user_actions.undo_move import undo_move


def get_menu_options():
    from user_actions.upload_sudoku import upload_sudoku
    from user_actions.load_saved_game import load_saved_game
    return {
        1: ("Start New Game", start_new_game),
        2: ("Upload Sudoku", upload_sudoku),
        3: ("Load Saved Game", load_saved_game),
        4: ("Exit", None)  # None handler indicates exiting the game
    }


def get_game_actions():
    return {
        "1": ("Make a move", make_a_move),
        "2": ("Get a hint", request_hint),
        "3": ("Undo last move", undo_move),
        "4": ("Solve the puzzle", solve_puzzle),
        "5": ("Save the game", lambda gs: (save_game_to_file(gs), gs)[1]),
        "6": ("Back to main menu", None)
    }
