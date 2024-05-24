import logging
import sys
from io import StringIO
from typing import Optional

from behave import given, when, then

from core_data.cell import Cell
from core_data.cell_state import CellState
from core_data.cell_value import CellValue
from core_data.coordinate import Coordinate
from core_data.game_state import GameState
from puzzle_handler.generate.generate_puzzle import generate_puzzle
from puzzle_handler.solve.puzzle_solver import update_grid, is_valid
from user_interface.display.display_grid import display_grid, display_messages
from utils.input_parsing import parse_user_input


# Helper functions
def make_a_move(game_state: GameState, user_input: str) -> Optional[GameState]:
    grid = game_state.grid
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
        print(f"Error: {e}")
        logging.error(f"ValueError: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        logging.error(f"Unexpected error: {e}", exc_info=True)
        return None
    return game_state


def validate_user_input(user_input: str, grid_size: int) -> bool:
    try:
        parse_user_input(user_input, grid_size)
        return True
    except ValueError:
        return False


def convert_parsed_moves(parsed_moves, grid_size):
    def convert_recursively(index, acc):
        if index >= len(parsed_moves):
            return acc
        (row, col), value = parsed_moves[index]
        state = CellState.USER_FILLED if value is not None else CellState.EMPTY
        acc.append((Coordinate(row, col, grid_size), Cell(CellValue(value, grid_size), state)))
        return convert_recursively(index + 1, acc)

    return convert_recursively(0, [])


def push_undo_recursively(game_state, moves, grid, index):
    if index >= len(moves):
        return game_state
    try:
        coord, _ = moves[index]
        undo_action = (coord.row_index, coord.col_index, grid[coord.row_index, coord.col_index].value.value)
        game_state = game_state.push_undo(undo_action)
    except Exception as e:
        logging.error(f"Error pushing undo: {e}")
        raise
    return push_undo_recursively(game_state, moves, grid, index + 1)


def apply_and_report_moves(grid, moves):
    messages = []
    grid = apply_moves_recursively(grid, moves, messages)
    return grid, messages


def apply_moves_recursively(grid, moves, messages, index=0):
    if index >= len(moves):
        return grid
    try:
        coord, cell = moves[index]
        current_cell = grid[coord.row_index, coord.col_index]
        if current_cell.state in {CellState.PRE_FILLED, CellState.HINT}:
            messages.append(
                f"Cannot apply move {chr(ord('A') + coord.row_index)}{coord.col_index + 1}={cell.value.value}. The cell is pre-filled or a hint.")
        else:
            grid = update_grid(grid, coord, cell.value.value,
                               CellState.USER_FILLED if cell.value.value is not None else CellState.EMPTY)
            messages.append(
                f"Move {chr(ord('A') + coord.row_index)}{coord.col_index + 1}={cell.value.value if cell.value.value is not None else 'None'} applied successfully.")
    except Exception as e:
        logging.error(f"Error applying move {index}: {e}")
        raise
    return apply_moves_recursively(grid, moves, messages, index + 1)


def has_empty_cells(grid):
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


def check_and_handle_completion(game_state):
    if is_puzzle_complete(game_state.grid):
        print("Congratulations! You Won")
        handle_completion_choice(game_state.config)
    return game_state


def is_puzzle_complete(grid):
    def check_cell(row, col):
        if row >= grid.grid_size:
            return True
        if col >= grid.grid_size:
            return check_cell(row + 1, 0)
        cell = grid[row, col]
        if cell.value.value is None or not is_valid(grid, row, col, cell.value.value):
            return False
        return check_cell(row, col + 1)

    return check_cell(0, 0)


def handle_completion_choice(config):
    choice = input("Want to Start a new Game (Yes/No): ").strip().lower()
    handle_choice_recursively(choice, config)


def handle_choice_recursively(choice, config):
    if choice == 'yes':
        from user_actions.start_new_game import start_new_game
        start_new_game(config)
    elif choice == 'no':
        return
    else:
        print("Invalid choice. Please enter 'Yes' or 'No'.")
        choice = input("Want to Start a new Game (Yes/No): ").strip().lower()
        handle_choice_recursively(choice, config)


# Given steps
@given('the game state is initialized')
def step_given_game_state_is_initialized(context):
    config = {"grid_size": 9}
    grid = generate_puzzle(config, "easy")
    context.game_state = GameState(grid, config)


@given('the current grid has a 5 in cell "A1"')
def step_given_grid_has_5_in_a1(context):
    coord = Coordinate(0, 0, context.game_state.grid.grid_size)
    cell = Cell(CellValue(5, context.game_state.grid.grid_size), CellState.PRE_FILLED)
    context.game_state.grid[coord] = cell


@given('the current grid has a pre-filled cell at "A1"')
def step_given_grid_has_pre_filled_cell_in_a1(context):
    coord = Coordinate(0, 0, context.game_state.grid.grid_size)
    cell = Cell(CellValue(5, context.game_state.grid.grid_size), CellState.PRE_FILLED)
    context.game_state.grid[coord] = cell


@given('the user has made a move "A1=5"')
def step_given_user_has_made_move_a1_5(context):
    context.game_state = make_a_move(context.game_state, "A1=5")


@given('the user has undone the last move "A1=5"')
def step_given_user_has_undone_last_move_a1_5(context):
    context.game_state.undo_stack.append((0, 0, 5))
    context.game_state.grid[Coordinate(0, 0, context.game_state.grid.grid_size)].value.value = None


@given('the Sudoku puzzle is almost complete')
def step_given_sudoku_puzzle_almost_complete(context):
    config = {"grid_size": 9}
    grid = generate_puzzle(config, "easy")
    for i in range(9):
        for j in range(9):
            if i == 8 and j == 8:
                continue
            coord = Coordinate(i, j, 9)
            grid[coord] = Cell(CellValue((i * 3 + j) % 9 + 1, 9), CellState.USER_FILLED)
    context.game_state = GameState(grid, config)


# When steps
@when('the user makes a valid move "A1=5"')
def step_when_user_makes_valid_move_a1_5(context):
    context.stdout = StringIO()
    sys.stdout = context.stdout
    context.game_state = make_a_move(context.game_state, "A1=5")
    context.make_a_move_output = context.stdout.getvalue().strip().split('\n')
    sys.stdout = sys.__stdout__


@when('the user makes an invalid move "A1=XYZ"')
def step_when_user_makes_invalid_move_a1_XYZ(context):
    context.stdout = StringIO()
    sys.stdout = context.stdout
    context.game_state = make_a_move(context.game_state, "A1=XYZ")
    context.make_a_move_output = context.stdout.getvalue().strip().split('\n')
    sys.stdout = sys.__stdout__


@when('the user makes the final valid move "I9=9"')
def step_when_user_makes_final_valid_move_I9_9(context):
    context.stdout = StringIO()
    sys.stdout = context.stdout
    context.game_state = make_a_move(context.game_state, "I9=9")
    context.make_a_move_output = context.stdout.getvalue().strip().split('\n')
    sys.stdout = sys.__stdout__


@when('the user undoes the last move')
def step_when_user_undoes_last_move(context):
    context.stdout = StringIO()
    sys.stdout = context.stdout
    undo_action, context.game_state = context.game_state.pop_undo()
    if undo_action:
        row, col, value = undo_action
        coord = Coordinate(row, col, context.game_state.grid.grid_size)
        context.game_state.grid[coord].value.value = value
        context.game_state = context.game_state.push_redo(undo_action)
    context.undo_output = context.stdout.getvalue().strip().split('\n')
    sys.stdout = sys.__stdout__


@when('the user redoes the last move')
def step_when_user_redoes_last_move(context):
    context.stdout = StringIO()
    sys.stdout = context.stdout
    redo_action, context.game_state = context.game_state.pop_redo()
    if redo_action:
        row, col, value = redo_action
        coord = Coordinate(row, col, context.game_state.grid.grid_size)
        context.game_state.grid[coord].value.value = value
        context.game_state = context.game_state.push_undo(redo_action)
    context.redo_output = context.stdout.getvalue().strip().split('\n')
    sys.stdout = sys.__stdout__


# Then steps
@then('the move is applied to the grid')
def step_then_move_applied_to_grid(context):
    coord = Coordinate(0, 0, context.game_state.grid.grid_size)
    assert context.game_state.grid[coord].value.value == 5, "The move was not applied to the grid."


@then('the move is pushed to the undo stack')
def step_then_move_pushed_to_undo_stack(context):
    assert context.game_state.undo_stack[-1] == (0, 0, 5), "The move was not pushed to the undo stack."


@then('the move is removed from the grid')
def step_then_move_removed_from_grid(context):
    coord = Coordinate(0, 0, context.game_state.grid.grid_size)
    assert context.game_state.grid[coord].value.value is None, "The move was not removed from the grid."


@then('the move is pushed to the redo stack')
def step_then_move_pushed_to_redo_stack(context):
    assert context.game_state.redo_stack[-1] == (0, 0, 5), "The move was not pushed to the redo stack."


@then('the move is reapplied to the grid')
def step_then_move_reapplied_to_grid(context):
    coord = Coordinate(0, 0, context.game_state.grid.grid_size)
    assert context.game_state.grid[coord].value.value == 5, "The move was not reapplied to the grid."


@then('the move is pushed back to the undo stack')
def step_then_move_pushed_back_to_undo_stack(context):
    assert context.game_state.undo_stack[-1] == (0, 0, 5), "The move was not pushed back to the undo stack."


@then('the system displays "{message}"')
def step_then_system_displays_message(context, message):
    assert message in context.make_a_move_output, f"Expected message: {message}, but got: {context.make_a_move_output}"


@then('prompts the user "Want to Start a new Game (Yes/No):"')
def step_then_prompts_user_for_new_game(context):
    assert "Want to Start a new Game (Yes/No):" in context.make_a_move_output, "Did not prompt for new game."
