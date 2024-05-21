from typing import Dict
from core_data.grid.grid import Grid
from core_data.coordinate import Coordinate
from puzzle_handler.generate.remove_cell import remove_cells_recursive
from puzzle_handler.solve.solve_puzzle import backtrack
from puzzle_handler.techniques.apply_naked_singles import apply_naked_singles
from puzzle_handler.solve.sudoku_validation import count_solutions
from utils.grid_utils import remove_cells


class PuzzleGenerationError(Exception):
    """Custom exception for errors during puzzle generation."""
    pass


def determine_cells_to_remove(grid_size: int, difficulty: str) -> int:
    """
    Determine the number of cells to remove based on the difficulty level.

    Args:
        grid_size (int): The size of the grid.
        difficulty (str): The difficulty level of the puzzle.

    Returns:
        int: The number of cells to remove.
    """
    difficulty_levels = {
        "easy": grid_size * grid_size // 4,
        "medium": grid_size * grid_size // 3,
        "hard": grid_size * grid_size // 2
    }
    return difficulty_levels.get(difficulty.lower(), grid_size * grid_size // 4)


def generate_puzzle(config: Dict, difficulty: str) -> Grid:
    """
    Generates a Sudoku puzzle based on the specified difficulty level.

    Args:
        config (Dict): Configuration settings.
        difficulty (str): Difficulty level of the puzzle.

    Returns:
        Grid: The generated Sudoku puzzle.

    Raises:
        PuzzleGenerationError: If the puzzle generation fails at any step.
    """
    try:
        grid_size = config['grid_size']
        if not isinstance(grid_size, int) or grid_size <= 0:
            raise ValueError("Invalid grid size specified in configuration.")

        # Create an empty grid using the Grid.create method
        grid = Grid.create(grid_size=grid_size, skip_validation=True)

        # Use backtracking to generate a complete Sudoku puzzle
        grid, success = backtrack(grid)
        if not success:
            raise PuzzleGenerationError("Failed to generate a valid Sudoku puzzle using backtracking.")

        # Apply naked singles technique to simplify the puzzle
        grid = apply_naked_singles(grid)

        # Determine the number of cells to remove based on difficulty
        num_cells_to_remove = determine_cells_to_remove(grid_size, difficulty)

        # Select balanced cells to remove
        cells_to_remove = remove_cells(grid_size, num_cells_to_remove)

        # Convert selected cells to Coordinate objects
        coordinates_to_remove = {Coordinate(row, col, grid_size) for row, col in cells_to_remove}

        # Remove cells to create the puzzle
        grid = remove_cells_recursive(coordinates_to_remove, grid, grid_size)

        # Ensure the puzzle has a unique solution
        if count_solutions(grid, grid_size) != 1:
            raise PuzzleGenerationError("Generated puzzle does not have a unique solution!")

        return grid

    except KeyError as e:
        raise PuzzleGenerationError(f"Missing configuration key: {e}")
    except ValueError as e:
        raise PuzzleGenerationError(f"Configuration error: {e}")
    except Exception as e:
        raise PuzzleGenerationError(f"An unexpected error occurred during puzzle generation: {e}")
