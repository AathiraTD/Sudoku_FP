import pytest
from unittest.mock import patch, MagicMock
from user_actions.start_new_game import start_new_game
from user_actions.request_hint import request_hint
from core_data.grid.grid import Grid
from core_data.game_state import GameState
from core_data.coordinate import Coordinate
from core_data.cell import Cell
from core_data.cell_value import CellValue
from core_data.cell_state import CellState


def test_start_new_game_and_request_hint(monkeypatch):
    def mock_input_start_new_game(prompt):
        return "1"  # Simulate choosing "Easy" difficulty

    def mock_get_hint_choice():
        return 'random'

    def mock_find_random_empty_cell(grid):
        return (0, 0)

    def mock_generate_hint(grid, row, col):
        return 1

    config = {
        'hint_limit': 3,
        'grid_size': 9,
        'difficulty_levels': {
            'easy': {'prefilled_cells': 36},
            'medium': {'prefilled_cells': 30},
            'hard': {'prefilled_cells': 24},
        }
    }

    monkeypatch.setattr('builtins.input', mock_input_start_new_game)

    # Mock the game_actions function to capture the game_state
    with patch('user_interface.game_actions.game_actions', new=MagicMock()) as mock_game_actions:
        game_state_holder = []

        def mock_game_actions_wrapper(game_state):
            game_state_holder.append(game_state)

        mock_game_actions.side_effect = mock_game_actions_wrapper

        start_new_game(config)

        # Ensure game_state is captured
        assert len(game_state_holder) == 1
        game_state = game_state_holder[0]

    # Ensure game_state is not None
    assert game_state is not None

    # Now simulate requesting a hint
    monkeypatch.setattr('user_actions.request_hint.get_hint_choice', mock_get_hint_choice)
    monkeypatch.setattr('utils.grid_utils.find_random_empty_cell', mock_find_random_empty_cell)
    monkeypatch.setattr('user_actions.request_hint.generate_hint', mock_generate_hint)

    request_hint(game_state)
    # No assertion needed; we just want to ensure no exceptions are raised

