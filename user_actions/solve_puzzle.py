from colorama import Fore, Style

from core_data.game_state import GameState
from core_data.grid import Grid
from puzzle_handler.puzzle_solver.puzzle_solver import backtrack, count_solutions
from user_interface.display.display_grid import display_grid
from user_interface.input.user_input_handler import get_post_solve_choice


def solve_puzzle(game_state: GameState) -> Grid:
    """
    Solve the Sudoku puzzle using backtracking.

    Args:
        grid (Grid): The Sudoku grid to puzzle_solver.

    Returns:
        Grid: The solved Sudoku grid.
        :param game_state:
    """
    grid = game_state.grid
    grid_size = grid.grid_size
    num_solutions = count_solutions(grid, grid_size)

    if num_solutions == 1:
        solved_grid, success = backtrack(grid)
        if success:
            # If the puzzle is successfully solved

            display_grid(solved_grid)  # Display the solved grid

            print(Fore.RED + Style.BRIGHT + "Puzzle solved successfully." + Style.RESET_ALL)

            choice = get_post_solve_choice()  # Get user's choice after solving
            if choice == 1:
                print("Starting a new game...")
                # Implement starting a new game logic here
            elif choice == 2:
                print("Returning to main menu...")
                # Implement returning to main menu logic here
            return solved_grid
        else:
            print("Failed to puzzle_solver the puzzle")
            return grid
    else:
        print(f"The puzzle has {num_solutions} solutions. It must have a unique solution to be solved. Please recheck "
              f" your moves.")
        return grid
