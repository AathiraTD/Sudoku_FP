from unittest.mock import mock_open, patch

import pytest

from config.config import load_config
from user_actions.upload_sudoku import upload_sudoku

# Mock configuration for the tests
config = {
    'hint_limit': 3,
    'grid_size': 9,
    'difficulty_levels': {
        'easy': {'prefilled_cells': 36},
        'medium': {'prefilled_cells': 30},
        'hard': {'prefilled_cells': 24},
    }
}

def test_upload_sudoku_valid(monkeypatch):
    valid_sudoku_content = (
        "5 3 0 0 7 0 0 0 0\n"
        "6 0 0 1 9 5 0 0 0\n"
        "0 9 8 0 0 0 0 6 0\n"
        "8 0 0 0 6 0 0 0 3\n"
        "4 0 0 8 0 3 0 0 1\n"
        "7 0 0 0 2 0 0 0 6\n"
        "0 6 0 0 0 0 2 8 0\n"
        "0 0 0 4 1 9 0 0 5\n"
        "0 0 0 0 8 0 0 7 9\n"
    )

    def mock_input(prompt):
        return "path/to/valid_sudoku.txt"  # Simulate file path input

    monkeypatch.setattr('builtins.input', mock_input)
    with patch("builtins.open", mock_open(read_data=valid_sudoku_content)):
        config = load_config("config/config.yaml")
        with patch('user_interface.display.display_grid') as mock_display_grid, \
             patch('user_interface.user_input.get_user_move', return_value='menu') as mock_get_user_move, \
             patch('user_interface.game_actions.game_actions') as mock_game_actions:
            upload_sudoku(config)
            mock_display_grid.assert_called()  # Ensure the grid was displayed
            mock_get_user_move.assert_called_once()  # Ensure the get_user_move was called
            mock_game_actions.assert_not_called()  # Ensure game_actions is not called because user chose menu

def test_upload_sudoku_invalid(monkeypatch):
    invalid_sudoku_content = (
        "5 3 0 0 7 0 0 0 0\n"
        "6 0 0 1 9 5 0 0 0\n"
        "0 9 8 0 0 0 0 6 0\n"
        "8 0 0 0 6 0 0 0 3\n"
        "4 0 0 8 0 3 0 0 1\n"
        "7 0 0 0 2 0 0 0 6\n"
        "0 6 0 0 0 0 2 8 0\n"
        "0 0 0 4 1 9 0 0 5\n"
        "0 0 0 0 8 0 0 7 10\n"  # Invalid: 10 is not a valid number for Sudoku
    )

    def mock_input(prompt):
        return "path/to/invalid_sudoku.txt"  # Simulate file path input

    monkeypatch.setattr('builtins.input', mock_input)
    with patch("builtins.open", mock_open(read_data=invalid_sudoku_content)):
        config = load_config("config/config.yaml")
        with patch('user_interface.display.display_grid') as mock_display_grid, \
             patch('user_interface.user_input.get_user_move', return_value='menu') as mock_get_user_move, \
             patch('user_interface.game_actions.game_actions') as mock_game_actions:
            with pytest.raises(ValueError, match="Invalid Sudoku puzzle provided"):
                upload_sudoku(config)
            mock_display_grid.assert_called()  # Ensure the grid was displayed
            mock_get_user_move.assert_not_called()  # Ensure the get_user_move was not called because of invalid grid
            mock_game_actions.assert_not_called()  # Ensure game_actions is not called due to invalid grid

# To run these specific test cases:
# pytest tests/user_actions/test_upload_sudoku.py
