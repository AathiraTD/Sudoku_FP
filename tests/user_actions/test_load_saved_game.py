import pytest
from user_actions.load_saved_game import load_saved_game

def test_load_saved_game(monkeypatch):
    def mock_prompt_for_load_location():
        return "path/to/saved/games"

    def mock_list_saved_game_files(directory):
        return ["saved_game_1.json"]

    def mock_prompt_for_file_choice(files):
        return "saved_game_1.json"

    def mock_validate_saved_game_file(file_path):
        return True

    monkeypatch.setattr('user_actions.load_saved_game.prompt_for_load_location', mock_prompt_for_load_location)
    monkeypatch.setattr('user_actions.load_saved_game.list_saved_game_files', mock_list_saved_game_files)
    monkeypatch.setattr('user_actions.load_saved_game.prompt_for_file_choice', mock_prompt_for_file_choice)
    monkeypatch.setattr('user_actions.load_saved_game.validate_saved_game_file', mock_validate_saved_game_file)

    config = {'hint_limit': 3}
    load_saved_game(config)
    # No assertion needed; we just want to ensure no exceptions are raised
