import pytest
from user_actions.start_new_game import start_new_game
from core_data.grid.grid import Grid
from unittest.mock import patch

def test_start_new_game_easy(monkeypatch):
    def mock_input(prompt):
        return "1"  # Simulate choosing "Easy" difficulty

    def mock_generate_puzzle(config, difficulty):
        cells = {}
        grid = Grid.create(grid_size=config['grid_size'])
        assert difficulty == 'easy'  # Ensure the difficulty is 'easy'
        return grid

    config = {
        'hint_limit': 3,
        'grid_size': 9,
        'difficulty_levels': {
            'easy': {'prefilled_cells': 36},
            'medium': {'prefilled_cells': 30},
            'hard': {'prefilled_cells': 24},
        }
    }

    monkeypatch.setattr('builtins.input', mock_input)
    monkeypatch.setattr('puzzle_handler.generate.generate_puzzle', mock_generate_puzzle)

    # Mock the game_actions function to prevent entering the game loop
    with patch('user_interface.game_actions.game_actions') as mock_game_actions:
        start_new_game(config)
        mock_game_actions.assert_called_once()

def test_start_new_game_medium(monkeypatch):
    def mock_input(prompt):
        return "2"  # Simulate choosing "Medium" difficulty

    def mock_generate_puzzle(config, difficulty):
        cells = {}
        grid = Grid.create(grid_size=config['grid_size'])
        assert difficulty == 'medium'  # Ensure the difficulty is 'medium'
        return grid

    config = {
        'hint_limit': 3,
        'grid_size': 9,
        'difficulty_levels': {
            'easy': {'prefilled_cells': 36},
            'medium': {'prefilled_cells': 30},
            'hard': {'prefilled_cells': 24},
        }
    }

    monkeypatch.setattr('builtins.input', mock_input)
    monkeypatch.setattr('puzzle_handler.generate.generate_puzzle', mock_generate_puzzle)

    # Mock the game_actions function to prevent entering the game loop
    with patch('user_interface.game_actions.game_actions') as mock_game_actions:
        start_new_game(config)
        mock_game_actions.assert_called_once()
