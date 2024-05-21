from typing import Optional, List, Tuple

from core_data.cell import Cell
from core_data.cell_state import CellState
from core_data.cell_value import CellValue
from core_data.coordinate import Coordinate
from core_data.grid.grid import Grid, update_cell
from user_interface.display.display_grid import display_grid, display_messages
from user_interface.user_input import get_user_move
from utils.input_parsing import parse_user_input


def make_a_move(grid: Grid) -> Optional[Grid]:
    """
    Main function to handle user moves.

    Args:
        grid (Grid): The Sudoku grid.

    Returns:
        Optional[Grid]: The updated grid after applying user moves, or None if an error occurred.
    """
    user_input = get_user_move()

    if not validate_user_input(user_input, grid.grid_size):
        print("Error: Invalid input format.")
        return None

    try:
        parsed_moves = parse_user_input(user_input, grid.grid_size)
        moves = convert_parsed_moves(parsed_moves, grid.grid_size)
        grid, messages = apply_and_report_moves(grid, moves)
        display_messages(messages)
        display_grid(grid)
    except ValueError as e:
        print(f"Error: {e}")
        return None

    return grid


def validate_user_input(user_input: str, grid_size: int) -> bool:
    """
    Validate the user's input.

    Args:
        user_input (str): The user's input.
        grid_size (int): The size of the Sudoku grid.

    Returns:
        bool: True if the input is valid, False otherwise.
    """
    # Add actual validation logic here
    return True


def convert_parsed_moves(parsed_moves: List[Tuple[Tuple[int, int], int]], grid_size: int) -> List[
    Tuple[Coordinate, Cell]]:
    """
    Convert parsed moves into a list of Coordinate and Cell tuples.

    Args:
        parsed_moves (List[Tuple[Tuple[int, int], int]]): The parsed moves.
        grid_size (int): The size of the Sudoku grid.

    Returns:
        List[Tuple[Coordinate, Cell]]: The converted list of moves.
    """

    def convert_recursively(index: int, acc: List[Tuple[Coordinate, Cell]]) -> List[Tuple[Coordinate, Cell]]:
        if index >= len(parsed_moves):  # Base case: all moves have been converted
            return acc
        (row, col), value = parsed_moves[index]
        acc.append((Coordinate(row, col, grid_size), Cell(CellValue(value, grid_size), CellState.USER_FILLED)))
        return convert_recursively(index + 1, acc)

    return convert_recursively(0, [])


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
        grid = update_cell(grid, coord, cell.value.value, CellState.USER_FILLED, skip_validation=True)
        messages.append(
            f"Move {chr(ord('A') + coord.row_index)}{coord.col_index + 1}={cell.value.value} applied successfully.")

    return apply_moves_recursively(grid, moves, messages, index + 1)
