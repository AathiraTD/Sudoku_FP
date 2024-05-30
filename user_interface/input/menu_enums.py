import importlib
from enum import Enum, auto


class BaseEnum(Enum):
    def __new__(cls, description, action):
        obj = object.__new__(cls)
        obj._value_ = auto()
        obj.description = description
        obj.action = action
        return obj


class MainMenuOption(BaseEnum):
    START_NEW_GAME = "Start New Game", "user_actions.start_new_game.start_new_game"
    UPLOAD_SUDOKU = "Upload Sudoku", "user_actions.upload_sudoku.upload_sudoku"
    LOAD_SAVED_GAME = "Load Saved Game", "user_actions.load_saved_game.load_saved_game"
    EXIT = "Exit", None


class DifficultyOption(BaseEnum):
    EASY = "Easy", None
    MEDIUM = "Medium", None
    HARD = "Hard", None


class PostSolveOption(BaseEnum):
    PLAY_NEW_GAME = "Play a new game", None
    RETURN_TO_MAIN_MENU = "Return to main menu", None


class HintOption(BaseEnum):
    RANDOM_CELL = "Random cell", None
    SPECIFIC_CELL = "Specific cell", None


class SaveLocationOption(BaseEnum):
    DEFAULT_LOCATION = "Default location (current directory)", None
    CUSTOM_LOCATION = "Custom location", None


class GameAction(BaseEnum):
    MAKE_A_MOVE = "Make a move", "user_actions.make_a_move.make_a_move"
    GET_A_HINT = "Get a hint", "user_actions.request_hint.request_hint"
    UNDO_LAST_MOVE = "Undo last move", "user_actions.undo_move.undo_move"
    SOLVE_PUZZLE = "Solve the puzzle", "user_actions.solve_puzzle.solve_puzzle"
    SAVE_GAME = "Save the game", "user_actions.save_game.save_game_to_file"
    BACK_TO_MAIN_MENU = "Back to main menu", None


def get_action_function(action_path):
    if not action_path:
        return None
    module_name, function_name = action_path.rsplit(".", 1)
    module = importlib.import_module(module_name)
    return getattr(module, function_name)


def generate_menu_options(enum_class):
    def recurse_options(enum_members, index=0):
        if index >= len(enum_members):
            return {}
        current_member = enum_members[index]
        action_function = get_action_function(current_member.action)
        return {index + 1: (current_member.description, action_function)} | recurse_options(enum_members, index + 1)

    return recurse_options(list(enum_class))


def get_menu_options(enum_class):
    return generate_menu_options(enum_class)
