import builtins
import sys
from io import StringIO

from behave import given, when, then

from core_data.cell import Cell
from core_data.cell_state import CellState
from core_data.cell_value import CellValue
from core_data.coordinate import Coordinate
from core_data.grid import Grid
from core_data.row import Row
from user_actions.request_hint import request_hint


# Helper to capture output
def capture_output(func, *args, **kwargs):
    old_stdout = sys.stdout
    sys.stdout = captured_output = StringIO()
    try:
        func(*args, **kwargs)
        return captured_output.getvalue()
    finally:
        sys.stdout = old_stdout




@given('there are empty cells in the grid')
def step_given_empty_cells_in_grid(context):
    empty = any(cell.value.value is None for row in context.game_state.grid.rows for cell in row.cells.values())
    assert empty, "No empty cells available"


@given('the user has not exceeded the hint limit')
def step_given_user_has_not_exceeded_hint_limit(context):
    context.game_state.hints_used = 0


@given('there are multiple empty cells in the grid')
def step_given_multiple_empty_cells(context):
    empty_cells = sum(
        1 for row in context.game_state.grid.rows for cell in row.cells.values() if cell.value.value is None)
    assert empty_cells > 1, "There are not multiple empty cells available"


@when('the user requests a hint for a specific empty cell')
def step_when_user_requests_hint_specific(context):
    # Simulate user input for a specific cell, e.g., "A1"
    def mock_input(prompt):
        return "A1"

    input_backup = builtins.input
    builtins.input = mock_input
    try:
        context.stdout = capture_output(request_hint, context.game_state)
    finally:
        builtins.input = input_backup
    context.hint_output = context.stdout.split('\n')


@then('the system analyzes the puzzle state')
def step_then_system_analyzes_puzzle_state(context):
    assert any("analyzes the puzzle state" in line.lower() for line in context.hint_output), \
        f"Expected analysis message, but got: {context.hint_output}"


@then('suggests possible numbers that can be placed in the selected cell')
def step_then_suggests_possible_numbers(context):
    assert any("possible numbers" in line.lower() for line in context.hint_output), \
        f"Expected possible numbers message, but got: {context.hint_output}"


@then('highlights the suggested cell on the grid')
def step_then_highlights_suggested_cell(context):
    assert any("highlights the suggested cell" in line.lower() for line in context.hint_output), \
        f"Expected highlight message, but got: {context.hint_output}"


@then('decreases the remaining hint count')
def step_then_decreases_remaining_hint_count(context):
    assert context.game_state.hints_used == 1, f"Expected hints used to be 1, but got: {context.game_state.hints_used}"


@when('the user requests a general hint')
def step_when_user_requests_general_hint(context):
    context.stdout = capture_output(request_hint, context.game_state)
    context.hint_output = context.stdout.split('\n')


@then('suggests a strategic move or provides guidance on solving a specific row, column, or subgrid')
def step_then_suggests_strategic_move(context):
    assert any("strategic move" in line.lower() or "guidance" in line.lower() for line in context.hint_output), \
        f"Expected strategic move or guidance message, but got: {context.hint_output}"


@then('highlights the area on the grid where the hint applies')
def step_then_highlights_hint_area(context):
    assert any("highlights the area" in line.lower() for line in context.hint_output), \
        f"Expected area highlight message, but got: {context.hint_output}"


@given('the user has used all available hints')
def step_given_user_used_all_hints(context):
    context.game_state.hints_used = context.game_state.config['hint_limit']


@then('the system notifies the user that the hint limit has been reached')
def step_then_notifies_hint_limit_reached(context):
    assert any("hint limit reached" in line.lower() for line in context.hint_output), \
        f"Expected hint limit message, but got: {context.hint_output}"


@then('no hint is provided')
def step_then_no_hint_provided(context):
    assert any("no hint" in line.lower() for line in context.hint_output), \
        f"Expected no hint message, but got: {context.hint_output}"


@given('there are no empty cells in the grid')
def step_given_no_empty_cells(context):
    # Fill all cells to simulate no empty cells
    new_rows = []
    for row in context.game_state.grid.rows:
        new_cells = {coord: Cell(value=CellValue(1, context.game_state.grid.grid_size), state=cell.state) for
                     coord, cell in row.cells.items()}
        new_row = Row.create(new_cells, row.row_index)
        new_rows.append(new_row)
    context.game_state.grid = Grid(rows=tuple(new_rows), grid_size=context.game_state.grid.grid_size)


@then('the system notifies the user that no empty cells are available for hints')
def step_then_notifies_no_empty_cells(context):
    assert any("no empty cells available" in line.lower() for line in context.hint_output), \
        f"Expected no empty cells message, but got: {context.hint_output}"


@given('the Sudoku puzzle is complete')
def step_given_puzzle_complete(context):
    # Simulate a complete puzzle
    new_rows = []
    for row in context.game_state.grid.rows:
        new_cells = {coord: Cell(value=CellValue(1, context.game_state.grid.grid_size), state=cell.state) for
                     coord, cell in row.cells.items()}
        new_row = Row.create(new_cells, row.row_index)
        new_rows.append(new_row)
    context.game_state.grid = Grid(rows=tuple(new_rows), grid_size=context.game_state.grid.grid_size)


@then('the system notifies the user that the puzzle is already complete')
def step_then_notifies_puzzle_complete(context):
    assert any("puzzle is already complete" in line.lower() for line in context.hint_output), \
        f"Expected puzzle complete message, but got: {context.hint_output}"


@given('the user selects a pre-filled cell for a hint')
def step_given_pre_filled_cell(context):
    # Simulate selecting a pre-filled cell
    coord = Coordinate(0, 0, context.game_state.grid.grid_size)
    cell = context.game_state.grid[coord]
    new_cell = Cell(value=cell.value, state=CellState.PRE_FILLED)
    new_cells = {c: (new_cell if c == coord else cell) for c, cell in
                 context.game_state.grid[coord.row_index].cells.items()}
    new_row = Row.create(new_cells, coord.row_index)
    new_rows = list(context.game_state.grid.rows)
    new_rows[coord.row_index] = new_row
    context.game_state.grid = Grid(rows=tuple(new_rows), grid_size=context.game_state.grid.grid_size)
    context.game_state.grid = Grid(rows=tuple(new_rows), grid_size=context.game_state.grid.grid_size)


@when('the user requests a hint for the pre-filled cell')
def step_when_user_requests_hint_pre_filled(context):
    context.stdout = capture_output(request_hint, context.game_state)
    context.hint_output = context.stdout.split('\n')


@then('the system notifies the user that the cell is pre-filled and cannot be modified')
def step_then_notifies_pre_filled_cell(context):
    assert any("cell is pre-filled and cannot be modified" in line.lower() for line in context.hint_output), \
        f"Expected pre-filled cell message, but got: {context.hint_output}"


@given('the user has made one or more moves on the Sudoku grid')
def step_given_user_made_moves(context):
    # Simulate making a move on the Sudoku grid
    coord = Coordinate(0, 1, context.game_state.grid.grid_size)
    cell = Cell(value=CellValue(5, context.game_state.grid.grid_size), state=CellState.USER_FILLED)
    context.game_state.grid = context.game_state.grid.with_updated_cell(coord, cell)
    context.previous_state = context.game_state.grid
#
# @when('the user selects the "Undo" option')
# def step_when_user_selects_undo(context):
#     context.stdout = capture_output(undo_move, context.game_state)
#     context.undo_output = context.stdout.split('\n')
#
# @then('the system should revert the grid to the state before the last move')
# def step_then_revert_grid
