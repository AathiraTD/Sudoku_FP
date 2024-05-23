from colorama import Fore, Style

from core_data.grid.grid import Grid
from puzzle_handler.solve.puzzle_solver import backtrack, count_solutions
from user_interface.display.display_grid import display_grid
from user_interface.user_input import get_post_solve_choice


def solve_puzzle(grid: Grid) -> Grid:
    """
    Solve the Sudoku puzzle using backtracking.

    Args:
        grid (Grid): The Sudoku grid to solve.

    Returns:
        Grid: The solved Sudoku grid.
    """
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
            print("Failed to solve the puzzle")
            return grid
    else:
        print(f"The puzzle has {num_solutions} solutions. It must have a unique solution to be solved. Please recheck "
              f" your moves.")
        return grid
