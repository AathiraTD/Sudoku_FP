from puzzle_handler.solve.backtrack import backtrack
from core_data.grid.grid import Grid
from puzzle_handler.solve.sudoku_validation import count_solutions
from user_interface.display.display_grid import display_grid


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
            print("Puzzle solved successfully.")
            display_grid(solved_grid)  # Display the solved grid
            return solved_grid
        else:
            print("Failed to solve the puzzle")
            return grid
    else:
        print(f"The puzzle has {num_solutions} solutions. It must have a unique solution to be solved. Please recheck "
              f" your moves.")
        return grid
