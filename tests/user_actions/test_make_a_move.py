from unittest.mock import patch

from core_data.cell import Cell
from core_data.cell_state import CellState
from core_data.cell_value import CellValue
from core_data.coordinate import Coordinate
from core_data.grid import Grid
from user_actions.make_a_move import make_a_move
from user_actions.start_new_game import start_new_game


def test_start_new_game_and_make_a_move(monkeypatch):
    def mock_input_start_new_game(prompt):
        return "1"  # Simulate choosing "Easy" difficulty

    def mock_generate_puzzle(config, difficulty):
        cells = {
            Coordinate(0, 0, 9): Cell(CellValue(None, 9), CellState.EMPTY),
            Coordinate(0, 1, 9): Cell(CellValue(3, 9), CellState.PRE_FILLED),
            Coordinate(1, 0, 9): Cell(CellValue(6, 9), CellState.PRE_FILLED),
        }
        grid = Grid(cells, config['grid_size'])
        assert difficulty == 'easy'  # Ensure the difficulty is 'easy'
        return grid

    def mock_get_user_move():
        return "A1=5"  # Simulate user entering a move

    def mock_parse_user_input(user_input, grid_size):
        return [((0, 0), 5)]  # Parse the move input

    def mock_convert_parsed_moves(parsed_moves, grid_size):
        return [(Coordinate(0, 0, 9), Cell(CellValue(5, 9), CellState.USER_FILLED))]

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
    monkeypatch.setattr('puzzle_handler.puzzle_generator.generate_puzzle', mock_generate_puzzle)

    # Mock the game_actions function to capture the game_state
    with patch('user_interface.game_actions.game_actions') as mock_game_actions:
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

    # Now simulate making a move
    monkeypatch.setattr('user_interface.user_input.get_user_move', mock_get_user_move)
    monkeypatch.setattr('user_actions.make_a_move.parse_user_input', mock_parse_user_input)
    monkeypatch.setattr('user_actions.make_a_move.convert_parsed_moves', mock_convert_parsed_moves)

    with patch('builtins.input', return_value='A1=5'):
        updated_game_state = make_a_move(game_state)
        # No assertion needed; we just want to ensure no exceptions are raised

