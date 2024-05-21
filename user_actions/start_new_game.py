from core_data.game_state import GameState
from user_interface.display.display_grid import display_grid

from user_interface.user_input import get_difficulty_choice
from puzzle_handler.generate.generate_puzzle import generate_puzzle


def start_new_game(config):

    from user_interface.game_actions import game_actions
    """
    Function to start a new game.
    """
    # Prompt user for difficulty level
    difficulty = get_difficulty_choice()

    # Generate the Sudoku puzzle based on the chosen difficulty
    grid = generate_puzzle(config, difficulty)

    # Initialize game state
    game_state = GameState(grid, config)

    # Display the generated Sudoku grid
    display_grid(game_state.grid)

    # Prompt for game actions
    game_actions(game_state)
