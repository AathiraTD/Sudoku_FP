import logging
from typing import Optional, List, Tuple, Dict

from core_data.cell import Cell
from core_data.cell_state import CellState
from core_data.cell_value import CellValue
from core_data.coordinate import Coordinate
from core_data.game_state import GameState
from core_data.grid.grid import Grid
from puzzle_handler.solve.puzzle_solver import is_valid
from puzzle_handler.solve.sudoku_validation import has_empty_cells, check_and_handle_completion
from user_interface.display.display_grid import display_grid, display_messages
from user_interface.user_input_handler import get_user_move
from utils.input_parsing import parse_user_input


def make_a_move(game_state: GameState) -> Optional[GameState]:
    """
    Make a move in the Sudoku game.

    Args:
        game_state (GameState): The current game state.

    Returns:
        Optional[GameState]: The updated game state if the move is valid, None otherwise.
    """
    grid = game_state.grid
    user_input = get_user_move()  # Get the user's move input

    if not validate_user_input(user_input, grid.grid_size):
        print("Error: Invalid input format.")  # Inform the user of invalid input format
        return None

    try:
        parsed_moves = parse_user_input(user_input, grid.grid_size)  # Parse the user input into moves
        moves = convert_parsed_moves(parsed_moves, grid.grid_size)  # Convert parsed moves to Coordinate and Cell

        # Push each move to the undo stack before applying moves
        game_state = push_undo_recursively(game_state, moves, grid, 0)

        # Clear the redo stack as new moves invalidate redo history
        game_state = game_state.clear_redo()

        # Apply the moves to the grid and collect messages
        grid, messages = apply_and_report_moves(grid, moves)

        # Display the messages and the updated grid
        display_messages(messages)
        display_grid(grid)

        # Update the game state with the new grid
        game_state = game_state.with_grid(grid)

        # Check if there are no empty cells left and handle puzzle completion
        if not has_empty_cells(grid):
            game_state = check_and_handle_completion(game_state)

    except ValueError as e:
        print(f"Error: {e}")
        logging.error(f"ValueError: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        logging.error(f"Unexpected error: {e}", exc_info=True)
        return None

    return game_state


def validate_user_input(user_input: str, grid_size: int) -> bool:
    """
    Validate the user input format.

    Args:
        user_input (str): The user's input string.
        grid_size (int): The size of the grid.

    Returns:
        bool: True if the input format is valid, False otherwise.
    """
    try:
        parse_user_input(user_input, grid_size)  # Try parsing the input
        return True
    except ValueError:
        return False


def convert_parsed_moves(parsed_moves: List[Tuple[Tuple[int, int], Optional[int]]], grid_size: int) -> List[
    Tuple[Coordinate, Cell]]:
    """
    Convert parsed moves to Coordinate and Cell objects.

    Args:
        parsed_moves (List[Tuple[Tuple[int, int], Optional[int]]]): Parsed moves.
        grid_size (int): The size of the grid.

    Returns:
        List[Tuple[Coordinate, Cell]]: List of coordinates and cells.
    """

    def convert_recursively(index: int, acc: List[Tuple[Coordinate, Cell]]) -> List[Tuple[Coordinate, Cell]]:
        if index >= len(parsed_moves):  # Base case: all moves have been converted
            return acc
        (row, col), value = parsed_moves[index]
        state = CellState.USER_FILLED if value is not None else CellState.EMPTY
        acc.append((Coordinate(row, col, grid_size), Cell(CellValue(value, grid_size), state)))
        return convert_recursively(index + 1, acc)

    return convert_recursively(0, [])


def push_undo_recursively(game_state: GameState, moves: List[Tuple[Coordinate, Cell]], grid: Grid,
                          index: int) -> GameState:
    """
    Push undo actions to the game state recursively.

    Args:
        game_state (GameState): The current game state.
        moves (List[Tuple[Coordinate, Cell]]): List of moves.
        grid (Grid): The current grid.
        index (int): Current index of the move to push.

    Returns:
        GameState: The updated game state.
    """
    if index >= len(moves):  # Base case: all moves have been pushed to undo stack
        return game_state

    try:
        coord, _ = moves[index]
        undo_action = (coord.row_index, coord.col_index, grid[coord].value.value)  # Access cell using grid indexing
        game_state = game_state.push_undo(undo_action)
    except Exception as e:
        logging.error(f"Error pushing undo: {e}")
        raise

    return push_undo_recursively(game_state, moves, grid, index + 1)


def apply_and_report_moves(grid: Grid, moves: List[Tuple[Coordinate, Cell]]) -> Tuple[Grid, List[str]]:
    """
    Apply moves to the grid and collect messages.

    Args:
        grid (Grid): The current grid.
        moves (List[Tuple[Coordinate, Cell]]): List of moves.

    Returns:
        Tuple[Grid, List[str]]: The updated grid and list of messages.
    """
    messages = []
    grid = apply_moves_recursively(grid, moves, messages)
    return grid, messages


def apply_moves_recursively(grid: Grid, moves: List[Tuple[Coordinate, Cell]], messages: List[str],
                            index: int = 0) -> Grid:
    """
    Recursively apply user moves to the grid.

    Args:
        grid (Grid): The Sudoku grid.
        moves (List[Tuple[Coordinate, Cell]]): A list of tuples containing coordinates and cells.
        messages (List[str]): List to store messages about the moves.
        index (int): The current index of the move to apply.

    Returns:
        Grid: The updated grid with moves applied.
    """
    if index >= len(moves):  # Base case: all moves have been applied
        return grid

    try:
        coord, cell = moves[index]
        current_cell = grid[coord]

        if current_cell.state in {CellState.PRE_FILLED, CellState.HINT}:
            messages.append(
                f"Cannot apply move {chr(ord('A') + coord.row_index)}{coord.col_index + 1}={cell.value.value}. The cell is pre-filled or a hint.")
        else:
            grid = grid.with_updated_cell(coord, cell)
            messages.append(
                f"Move {chr(ord('A') + coord.row_index)}{coord.col_index + 1}={cell.value.value if cell.value.value is not None else 'None'} applied successfully.")
    except Exception as e:
        logging.error(f"Error applying move {index}: {e}")
        raise

    return apply_moves_recursively(grid, moves, messages, index + 1)


def has_empty_cells(grid: Grid) -> bool:
    def check_rows_recursively(rows, row_index, col_index, grid_size):
        if row_index >= len(rows):
            return False
        if col_index >= grid_size:
            return check_rows_recursively(rows, row_index + 1, 0, grid_size)

        cell = grid[Coordinate(row_index, col_index, grid_size)]
        if cell.state == CellState.EMPTY:
            return True

        return check_rows_recursively(rows, row_index, col_index + 1, grid_size)

    return check_rows_recursively(grid.rows, 0, 0, grid.grid_size)


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
        cell = grid[Coordinate(row, col, grid.grid_size)]
        if cell.value.value is None or not is_valid(grid, row, col, cell.value.value):
            return False
        return check_cell(row, col + 1)

    return check_cell(0, 0)


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
    from user_actions import start_new_game
    if choice == 'yes':
        start_new_game(config)  # Assuming start_new_game is defined elsewhere
    elif choice == 'no':
        return  # Exit the recursion
    else:
        print("Invalid choice. Please enter 'Yes' or 'No'.")
        choice = input("Want to Start a new Game (Yes/No): ").strip().lower()
        handle_choice_recursively(choice, config)
