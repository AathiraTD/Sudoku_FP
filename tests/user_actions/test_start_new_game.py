import unittest
from unittest.mock import patch, MagicMock

from user_actions.start_new_game import start_new_game


class TestStartNewGame(unittest.TestCase):
    def setUp(self):
        # Configuration settings
        self.config = {'grid_size': 9}

    @patch('start_new_game_module.get_difficulty_choice')
    @patch('start_new_game_module.display_invalid_input')
    def test_invalid_difficulty_input(self, mock_display_invalid_input, mock_get_difficulty_choice):
        # Simulate invalid difficulty input
        mock_get_difficulty_choice.return_value = 'invalid'

        # Run the start_new_game function
        start_new_game(self.config)

        # Assert invalid input message is displayed
        mock_display_invalid_input.assert_called_once_with("Invalid input. Please enter a number between 1 and 3.")

    @patch('start_new_game_module.get_difficulty_choice')
    @patch('start_new_game_module.generate_puzzle')
    @patch('start_new_game_module.initialize_game_state')
    @patch('start_new_game_module.display_grid')
    @patch('start_new_game_module.prompt_for_game_actions')
    def test_start_new_game(self, mock_prompt_for_game_actions, mock_display_grid, mock_initialize_game_state,
                            mock_generate_puzzle, mock_get_difficulty_choice):
        # Simulate valid difficulty input
        mock_get_difficulty_choice.return_value = 'easy'

        # Mocking the return values for generate_puzzle and initialize_game_state
        mock_grid = MagicMock()
        mock_game_state = MagicMock()
        mock_generate_puzzle.return_value = mock_grid
        mock_initialize_game_state.return_value = mock_game_state

        # Run the start_new_game function
        start_new_game(self.config)

        # Assert the functions are called with expected arguments
        mock_generate_puzzle.assert_called_once_with(self.config, 'easy')
        mock_initialize_game_state.assert_called_once_with(mock_grid, self.config)
        mock_display_grid.assert_called_once_with(mock_game_state.grid)
        mock_prompt_for_game_actions.assert_called_once_with(mock_game_state)


if __name__ == "__main__":
    unittest.main()
