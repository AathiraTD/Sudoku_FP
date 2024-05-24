from typing import Dict

from core_data.coordinate import Coordinate
from core_data.grid.grid import Grid
from puzzle_handler.generate.remove_cell import remove_cells_recursive
from puzzle_handler.solve.puzzle_solver import backtrack, count_solutions
from puzzle_handler.techniques.apply_naked_singles import apply_naked_singles
from utils.grid_utils import remove_cells


class PuzzleGenerationError(Exception):
    pass

def determine_cells_to_remove(grid_size: int, difficulty: str) -> int:
    difficulty_levels = {
        "easy": grid_size * grid_size // 4,
        "medium": grid_size * grid_size // 3,
        "hard": grid_size * grid_size // 2
    }
    return difficulty_levels.get(difficulty.lower(), grid_size * grid_size // 4)

def generate_puzzle(config: Dict, difficulty: str) -> Grid:
    grid_size = config.get('grid_size', 9)
    validate_grid_size(grid_size)
    grid = create_and_solve_grid(grid_size)
    grid = apply_naked_singles(grid)
    num_cells_to_remove = determine_cells_to_remove(grid_size, difficulty)
    coordinates_to_remove = select_cells_to_remove(grid_size, num_cells_to_remove)
    grid = remove_cells_recursive(coordinates_to_remove, grid, grid_size)
    ensure_unique_solution(grid, grid_size)
    return grid


def validate_grid_size(grid_size: int):
    if not isinstance(grid_size, int) or grid_size <= 0:
        raise ValueError("Invalid grid size specified in configuration.")


def create_and_solve_grid(grid_size: int) -> Grid:
    grid = Grid.create(grid_size=grid_size)
    grid, success = backtrack(grid)
    if not success:
        raise PuzzleGenerationError("Failed to generate a valid Sudoku puzzle using backtracking.")
    return grid


def select_cells_to_remove(grid_size: int, num_cells_to_remove: int) -> set:
    cells_to_remove = remove_cells(grid_size, num_cells_to_remove)
    return {Coordinate(row, col, grid_size) for row, col in cells_to_remove}


def ensure_unique_solution(grid: Grid, grid_size: int):
    if count_solutions(grid, grid_size) != 1:
        raise PuzzleGenerationError("Generated puzzle does not have a unique solution!")
