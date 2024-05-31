import logging
from typing import List, Optional, Tuple

from core_data.cell import Cell
from core_data.cell_state import CellState
from core_data.coordinate import Coordinate
from core_data.game_state import GameState
from core_data.grid import Grid
from gherkin_spec.make_a_move_steps import convert_parsed_moves, apply_and_report_moves, validate_user_input
from puzzle_handler.puzzle_solver.puzzle_solver import is_valid
from puzzle_handler.puzzle_solver.sudoku_validation import has_empty_cells, check_and_handle_completion
from user_interface.display.display_grid import display_grid, display_messages
from user_interface.input.user_input_handler import get_user_move
from utils.input_parsing import parse_user_input


def make_a_move(game_state: GameState) -> Optional[GameState]:
    grid = game_state.grid
    user_input = get_user_move()

    if not validate_user_input(user_input, grid.grid_size):
        print("Error: Invalid input format.")
        return None

    try:
        parsed_moves = parse_user_input(user_input, grid.grid_size)
        moves = convert_parsed_moves(parsed_moves, grid.grid_size)

        game_state = push_undo_recursively(game_state, moves, grid, 0)
        game_state = game_state.clear_redo()

        grid, messages = apply_and_report_moves(grid, moves)

        display_messages(messages)
        display_grid(grid)

        game_state = game_state.with_grid(grid)

        if not has_empty_cells(grid):
            game_state = check_and_handle_completion(game_state)

    except ValueError as e:
        error_message = f"Error: {e}"
        display_messages([error_message])
        logging.error(f"ValueError: {e}")
        return game_state
    except Exception as e:
        error_message = f"An unexpected error occurred: {e}"
        display_messages([error_message])
        logging.error(f"Unexpected error: {e}", exc_info=True)
        return game_state

    return game_state


def push_undo_recursively(game_state: GameState, moves: List[Tuple[Coordinate, Cell]], grid: Grid,
                          index: int) -> GameState:
    if index >= len(moves):
        return game_state

    try:
        coord, _ = moves[index]
        undo_action = (coord.row_index, coord.col_index, grid[coord].value.value)
        game_state = game_state.push_undo(undo_action)
    except Exception as e:
        logging.error(f"Error pushing undo: {e}")
        raise

    return push_undo_recursively(game_state, moves, grid, index + 1)


def is_puzzle_complete(grid: Grid) -> bool:
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


def apply_moves_recursively(grid: Grid, moves: List[Tuple[Coordinate, Cell]], messages: List[str],
                            index: int = 0) -> Grid:
    if index >= len(moves):
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
