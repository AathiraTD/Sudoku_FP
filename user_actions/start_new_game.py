from core_data.game_state import GameState
from puzzle_handler.generate.generate_puzzle import generate_puzzle
from user_interface.display.display_grid import display_grid
from user_interface.display.menu_display import display_invalid_input
from user_interface.input.user_input_handler import get_difficulty_choice


def start_new_game(config):
    """
    Function to start a new game.
    """
    difficulty = get_difficulty_choice()
    if difficulty not in ["easy", "medium", "hard"]:
        display_invalid_input("Invalid input. Please enter a number between 1 and 3.")
        return
    grid = generate_puzzle(config, difficulty)
    game_state = initialize_game_state(grid, config)
    display_grid(game_state.grid)
    prompt_for_game_actions(game_state)


def initialize_game_state(grid, config):
    """
    Initialize the game state with the given grid and config.

    Args:
        grid: The generated Sudoku grid.
        config: Configuration settings.

    Returns:
        GameState: The initialized game state.
    """
    return GameState(grid, config)


def prompt_for_game_actions(game_state):
    """
    Prompt for game actions.

    Args:
        game_state: The current state of the game.
    """
    from user_interface.controller.game_actions_controller import game_actions
    game_actions(game_state)
