from typing import Optional, List, Tuple
from core_data.cell import Cell
from core_data.cell_state import CellState
from core_data.cell_value import CellValue
from core_data.coordinate import Coordinate
from core_data.grid.grid import Grid, update_cell
from core_data.game_state import GameState
from puzzle_handler.solve.sudoku_validation import has_empty_cells, check_and_handle_completion
from user_interface.display.display_grid import display_grid, display_messages
from user_interface.user_input import get_user_move
from utils.grid_utils import label_to_index
from utils.input_parsing import parse_user_input


def make_a_move(game_state: GameState) -> Optional[GameState]:
    """
    Main function to handle user moves.

    Args:
        game_state (GameState): The current state of the game.

    Returns:
        Optional[GameState]: The updated game state after applying user moves, or None if an error occurred.
    """
    grid = game_state.grid
    user_input = get_user_move()

    if not validate_user_input(user_input, grid.grid_size):
        print("Error: Invalid input format.")
        return None

    try:
        parsed_moves = parse_user_input(user_input, grid.grid_size)
        moves = convert_parsed_moves(parsed_moves, grid.grid_size)

        # Push each move to the undo stack before applying moves
        game_state = push_undo_recursively(game_state, moves, grid, 0)

        # Clear the redo stack as new moves invalidate redo history
        game_state = game_state.clear_redo()

        grid, messages = apply_and_report_moves(grid, moves)
        display_messages(messages)
        display_grid(grid)

        game_state = game_state.with_grid(grid)

        if not has_empty_cells(grid):  # Check for empty cells before triggering completion check
            game_state = check_and_handle_completion(game_state)

    except ValueError as e:
        print(f"Error: {e}")
        return None

    return game_state


def validate_user_input(user_input: str, grid_size: int) -> bool:
    """
    Validate the user's input.

    Args:
        user_input (str): The user's input.
        grid_size (int): The size of the Sudoku grid.

    Returns:
        bool: True if the input is valid, False otherwise.
    """
    try:
        parse_user_input(user_input, grid_size)
        return True
    except ValueError:
        return False


def convert_parsed_moves(parsed_moves: List[Tuple[Tuple[int, int], Optional[int]]], grid_size: int) -> List[
    Tuple[Coordinate, Cell]]:
    """
    Convert parsed moves into a list of Coordinate and Cell tuples.

    Args:
        parsed_moves (List[Tuple[Tuple[int, int], Optional[int]]]): The parsed moves.
        grid_size (int): The size of the Sudoku grid.

    Returns:
        List[Tuple[Coordinate, Cell]]: The converted list of moves.
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
    Recursively push each move to the undo stack.

    Args:
        game_state (GameState): The current state of the game.
        moves (List[Tuple[Coordinate, Cell]]): The list of moves.
        grid (Grid): The current state of the grid.
        index (int): The current index of the move to process.

    Returns:
        GameState: The updated game state with the undo stack.
    """
    if index >= len(moves):  # Base case: all moves have been pushed to undo stack
        return game_state

    coord, _ = moves[index]
    undo_action = (coord.row_index, coord.col_index, grid.cells[coord].value.value)
    game_state = game_state.push_undo(undo_action)

    return push_undo_recursively(game_state, moves, grid, index + 1)


def apply_and_report_moves(grid: Grid, moves: List[Tuple[Coordinate, Cell]]) -> Tuple[Grid, List[str]]:
    """
    Apply user moves to the grid and return messages about the moves.

    Args:
        grid (Grid): The Sudoku grid.
        moves (List[Tuple[Coordinate, Cell]]): A list of tuples containing coordinates and cells.

    Returns:
        Tuple[Grid, List[str]]: The updated grid and a list of messages about the moves.
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

    coord, cell = moves[index]
    current_cell = grid.cells[coord]

    if current_cell.state in {CellState.PRE_FILLED, CellState.HINT}:
        messages.append(
            f"Cannot apply move {chr(ord('A') + coord.row_index)}{coord.col_index + 1}={cell.value.value}. The cell is pre-filled or a hint.")
    else:
        grid = update_cell(grid, coord, cell.value.value, CellState.USER_FILLED if cell.value.value is not None else CellState.EMPTY, skip_validation=True)
        messages.append(
            f"Move {chr(ord('A') + coord.row_index)}{coord.col_index + 1}={cell.value.value if cell.value.value is not None else 'None'} applied successfully.")

    return apply_moves_recursively(grid, moves, messages, index + 1)


def parse_user_input(user_input: str, grid_size: int) -> List[Tuple[Tuple[int, int], Optional[int]]]:
    """
    Parse user input into a list of (coordinate, value) tuples.

    Args:
        user_input (str): The user's input string.
        grid_size (int): The size of the grid.

    Returns:
        List[Tuple[Tuple[int, int], Optional[int]]]: A list of parsed (coordinate, value) tuples.
    """
    moves = user_input.split(',')
    parsed_moves = []

    def parse_move(move_list: List[str], acc: List[Tuple[Tuple[int, int], Optional[int]]]) -> List[Tuple[Tuple[int, int], Optional[int]]]:
        if not move_list:
            return acc  # Base case: all moves have been parsed

        move = move_list[0].strip()
        if '=' not in move:
            raise ValueError(f"Invalid input format: {move}")

        position, value = move.split('=')
        coord = label_to_index(position.strip(), grid_size)
        if coord is None:
            raise ValueError(f"Invalid cell coordinate: {position}")
        if value.strip().lower() == 'none':
            acc.append((coord, None))
        elif value.strip().isdigit():
            acc.append((coord, int(value.strip())))
        else:
            raise ValueError(f"Invalid cell value: {value}")

        return parse_move(move_list[1:], acc)  # Recursively parse the next move

    return parse_move(moves, parsed_moves)  # Start parsing from the first move
