import pytest
from core_data.cell import Cell, CellValue, CellState
from core_data.coordinate import Coordinate
from core_data.grid.grid import Grid
from core_data.game_state import GameState


def test_game_state_creation():
    cells = {
        Coordinate(0, 0, 9): Cell(CellValue(1, 9), CellState.PRE_FILLED),
        Coordinate(1, 1, 9): Cell(CellValue(2, 9), CellState.USER_FILLED),
    }
    grid = Grid(cells, 9)
    config = {'hint_limit': 3}
    game_state = GameState(grid, config)
    assert game_state.grid == grid
    assert game_state.config == config
    assert game_state.hints_used == 0
    assert game_state.undo_stack == []
    assert game_state.redo_stack == []


def test_game_state_increment_hints():
    cells = {
        Coordinate(0, 0, 9): Cell(CellValue(1, 9), CellState.PRE_FILLED),
    }
    grid = Grid(cells, 9)
    config = {'hint_limit': 3}
    game_state = GameState(grid, config)
    new_game_state = game_state.increment_hints()
    assert new_game_state.hints_used == 1


def test_game_state_reset_hints():
    cells = {
        Coordinate(0, 0, 9): Cell(CellValue(1, 9), CellState.PRE_FILLED),
    }
    grid = Grid(cells, 9)
    config = {'hint_limit': 3}
    game_state = GameState(grid, config, hints_used=2)
    new_game_state = game_state.reset_hints()
    assert new_game_state.hints_used == 0


def test_game_state_hints_remaining():
    cells = {
        Coordinate(0, 0, 9): Cell(CellValue(1, 9), CellState.PRE_FILLED),
    }
    grid = Grid(cells, 9)
    config = {'hint_limit': 3}
    game_state = GameState(grid, config, hints_used=2)
    assert game_state.hints_remaining() == 1


def test_game_state_can_use_hint():
    cells = {
        Coordinate(0, 0, 9): Cell(CellValue(1, 9), CellState.PRE_FILLED),
    }
    grid = Grid(cells, 9)
    config = {'hint_limit': 3}
    game_state = GameState(grid, config, hints_used=3)
    assert not game_state.can_use_hint()
    game_state = GameState(grid, config, hints_used=2)
    assert game_state.can_use_hint()


def test_game_state_with_grid():
    cells = {
        Coordinate(0, 0, 9): Cell(CellValue(1, 9), CellState.PRE_FILLED),
    }
    grid = Grid(cells, 9)
    config = {'hint_limit': 3}
    game_state = GameState(grid, config)
    new_cells = {
        Coordinate(0, 0, 9): Cell(CellValue(2, 9), CellState.USER_FILLED),
    }
    new_grid = Grid(new_cells, 9)
    new_game_state = game_state.with_grid(new_grid)
    assert new_game_state.grid == new_grid


def test_game_state_push_undo():
    cells = {
        Coordinate(0, 0, 9): Cell(CellValue(1, 9), CellState.PRE_FILLED),
    }
    grid = Grid(cells, 9)
    config = {'hint_limit': 3}
    game_state = GameState(grid, config)
    action = (0, 0, 1)
    new_game_state = game_state.push_undo(action)
    assert new_game_state.undo_stack == [action]


def test_game_state_pop_undo():
    cells = {
        Coordinate(0, 0, 9): Cell(CellValue(1, 9), CellState.PRE_FILLED),
    }
    grid = Grid(cells, 9, skip_validation=True)
    config = {'hint_limit': 3}
    game_state = GameState(grid, config)
    action = (0, 0, 1)
    game_state = game_state.push_undo(action)
    popped_action, new_game_state = game_state.pop_undo()
    assert popped_action == action
    assert new_game_state.undo_stack == []


def test_game_state_push_redo():
    cells = {
        Coordinate(0, 0, 9): Cell(CellValue(1, 9), CellState.PRE_FILLED),
    }
    grid = Grid(cells, 9, skip_validation=True)
    config = {'hint_limit': 3}
    game_state = GameState(grid, config)
    action = (0, 0, 1)
    new_game_state = game_state.push_redo(action)
    assert new_game_state.redo_stack == [action]


def test_game_state_pop_redo():
    cells = {
        Coordinate(0, 0, 9): Cell(CellValue(1, 9), CellState.PRE_FILLED),
    }
    grid = Grid(cells, 9, skip_validation=True)
    config = {'hint_limit': 3}
    game_state = GameState(grid, config)
    action = (0, 0, 1)
    game_state = game_state.push_redo(action)
    popped_action, new_game_state = game_state.pop_redo()
    assert popped_action == action
    assert new_game_state.redo_stack == []


def test_game_state_clear_redo():
    cells = {
        Coordinate(0, 0, 9): Cell(CellValue(1, 9), CellState.PRE_FILLED),
    }
    grid = Grid(cells, 9, skip_validation=True)
    config = {'hint_limit': 3}
    game_state = GameState(grid, config)
    action = (0, 0, 1)
    game_state = game_state.push_redo(action)
    new_game_state = game_state.clear_redo()
    assert new_game_state.redo_stack == []
