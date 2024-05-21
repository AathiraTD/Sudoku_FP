from user_interface.display.display_grid import display_grid
from user_interface.game_actions import game_actions
from user_interface.user_input import get_difficulty_choice
from puzzle_handler.generate.generate_puzzle import generate_puzzle


def start_new_game(config):
    """
    Function to start a new game.
    """
    # Prompt user for difficulty level
    difficulty = get_difficulty_choice()

    # Generate the Sudoku puzzle based on the chosen difficulty
    grid = generate_puzzle(config, difficulty)

    # Display the generated Sudoku grid
    display_grid(grid)

    # Prompt for game actions
    game_actions(config, grid)
