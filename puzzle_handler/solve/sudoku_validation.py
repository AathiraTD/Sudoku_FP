from typing import Tuple,  Dict
from core_data.cell import Cell
from core_data.cell_state import CellState
from core_data.game_state import GameState
from core_data.grid.grid import Grid
from core_data.coordinate import Coordinate
import user_actions.start_new_game
from puzzle_handler.solve.puzzle_solver import is_valid

# Custom cache dictionary
count_solutions_cache: Dict[Tuple, int] = {}


def validate_move(grid: Grid, move: Tuple[Coordinate, Cell]) -> Tuple[bool, str]:
    """
    Validate a single user move.

    Args:
        grid (Grid): The Sudoku grid.
        move (Tuple[Coordinate, Cell]): A tuple containing the coordinate and the cell to be validated.

    Returns:
        Tuple[bool, str]: A tuple with a boolean indicating validity and a message.
    """
    coord, cell = move
    row, col = coord.row_index, coord.col_index
    value = cell.value.value

    if not (1 <= value <= grid.grid_size):
        return False, f"Invalid value: {value}. Must be between 1 and {grid.grid_size}."
    if not is_valid(grid, row, col, value, grid.grid_size):
        return False, f"Invalid move at {chr(ord('A') + row)}{col + 1}. Does not satisfy Sudoku rules."
    return True, f"Move {chr(ord('A') + row)}{col + 1}={value} applied successfully."


def is_puzzle_complete(grid: Grid) -> bool:
    """
    Check if the Sudoku puzzle is complete and valid.

    Args:
        grid (Grid): The Sudoku grid.

    Returns:
        bool: True if the puzzle is complete and valid, False otherwise.
    """

    def check_cell(row: int, col: int) -> bool:
        if row >= grid.grid_size:
            return True
        if col >= grid.grid_size:
            return check_cell(row + 1, 0)
        cell = grid.cells[Coordinate(row, col, grid.grid_size)]
        if cell.value.value is None or not is_valid(grid, row, col, cell.value.value, grid.grid_size):
            return False
        return check_cell(row, col + 1)

    return check_cell(0, 0)


def check_and_handle_completion(game_state: GameState) -> GameState:
    """
    Check if the puzzle is complete and handle the completion scenario.

    Args:
        game_state (GameState): The current state of the game.

    Returns:
        GameState: The updated game state.
    """
    if is_puzzle_complete(game_state.grid):
        print("Congratulations! You Won")
        handle_completion_choice(game_state.config)
    return game_state


def handle_completion_choice(config: Dict) -> None:
    """
    Handle the user's choice after completing the puzzle.

    Args:
        config (Dict): The game configuration.
    """
    choice = input("Want to Start a new Game (Yes/No): ").strip().lower()
    handle_choice_recursively(choice, config)


def handle_choice_recursively(choice: str, config: Dict) -> None:
    """
    Recursively handle the user's choice for starting a new game or returning to the main menu.

    Args:
        choice (str): The user's choice.
        config (Dict): The game configuration.
    """
    if choice == 'yes':
        user_actions.start_new_game.start_new_game(config)  # Assuming start_new_game is defined elsewhere
    elif choice == 'no':
        return  # Exit the recursion
    else:
        print("Invalid choice. Please enter 'Yes' or 'No'.")
        choice = input("Want to Start a new Game (Yes/No): ").strip().lower()
        handle_choice_recursively(choice, config)


def has_empty_cells(grid: Grid) -> bool:
    def check_rows_recursively(rows, row_index, col_index, grid_size):
        if row_index >= len(rows):
            return False
        if col_index >= grid_size:
            return check_rows_recursively(rows, row_index + 1, 0, grid_size)

        cell = grid[row_index, col_index]
        if cell.state == CellState.EMPTY:
            return True

        return check_rows_recursively(rows, row_index, col_index + 1, grid_size)

    return check_rows_recursively(grid.rows, 0, 0, grid.grid_size)
