import pytest
import os
import json
from user_actions.save_game import save_game_to_file
from core_data.grid.grid import Grid
from puzzle_handler.generate.generate_puzzle import generate_puzzle

def test_save_game_to_file(monkeypatch, tmpdir):
    # Create a temporary directory to save the file
    save_path = tmpdir.mkdir("saved_games")

    def mock_prompt_for_file_details():
        return ("test_game.json", str(save_path))

    monkeypatch.setattr('user_actions.save_game.prompt_for_file_details', mock_prompt_for_file_details)

    # Configuration for the puzzle
    config = {
        'hint_limit': 3,
        'grid_size': 9,
        'difficulty_levels': {
            'easy': {'prefilled_cells': 36},
            'medium': {'prefilled_cells': 30},
            'hard': {'prefilled_cells': 24},
        }
    }

    # Generate a puzzle
    grid = generate_puzzle(config, 'hard')

    # Ensure the grid is generated correctly
    assert isinstance(grid, Grid)
    assert grid.grid_size == 9

    # Save the game to a file
    save_game_to_file(grid)

    # Verify that the file was saved
    saved_file_path = os.path.join(str(save_path), "test_game.json")
    assert os.path.exists(saved_file_path)

    # Load and verify the content of the saved file
    with open(saved_file_path, 'r') as file:
        saved_data = json.load(file)
        assert 'cells' in saved_data
        assert 'grid_size' in saved_data
        assert saved_data['grid_size'] == 9

        # Verify some cell data
        for key, cell in saved_data['cells'].items():
            coord = eval(key)
            assert 'value' in cell
            assert 'state' in cell
            assert cell['value'] is None or (1 <= cell['value'] <= 9)
            assert cell['state'] in ['EMPTY', 'PRE_FILLED', 'USER_FILLED', 'FIXED']

# To run this specific test file:
# pytest tests/user_actions/test_save_game_to_file.py
