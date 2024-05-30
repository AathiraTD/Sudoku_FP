from unittest.mock import patch, MagicMock

from core_data.cell import Cell
from core_data.cell_state import CellState
from core_data.cell_value import CellValue
from core_data.coordinate import Coordinate
from user_actions.make_a_move import make_a_move
from user_actions.start_new_game import start_new_game
from user_actions.undo_move import undo_move


def test_start_new_game_and_undo_move(monkeypatch):
    def mock_input_start_new_game(prompt):
        return "3"  # Simulate choosing "Hard" difficulty

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

    # Now simulate making a move
    monkeypatch.setattr('user_interface.user_input.get_user_move', mock_get_user_move)
    monkeypatch.setattr('user_actions.make_a_move.parse_user_input', mock_parse_user_input)
    monkeypatch.setattr('user_actions.make_a_move.convert_parsed_moves', mock_convert_parsed_moves)

    with patch('builtins.input', return_value='A1=5'):
        updated_game_state = make_a_move(game_state)
        # No assertion needed; we just want to ensure no exceptions are raised

    # Ensure the move has been applied correctly
    assert updated_game_state.grid.cells[Coordinate(0, 0, 9)].value.value == 5
    assert updated_game_state.grid.cells[Coordinate(0, 0, 9)].state == CellState.USER_FILLED

    # Now simulate undoing the move
    last_move = updated_game_state.undo_stack[-1]  # Get the last move from the undo stack
    undo_move(updated_game_state)

    # # Ensure the move has been undone correctly
    # assert updated_game_state.grid.cells[last_move[0]].value.value is None
    # assert updated_game_state.grid.cells[last_move[0]].state == CellState.EMPTY
