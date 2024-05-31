import os
import sys
from unittest.mock import patch

from behave import given, when, then

# Adding the project root to the system path to enable module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# Correct import path based on the provided directory structure
from user_interface.controller import main_menu_controller


# Mock functions and classes
@patch('user_interface.controller.main_menu_controller.clear_screen')
@patch('user_interface.controller.main_menu_controller.display_menu_with_title')
@patch('user_interface.controller.main_menu_controller.prompt_choice')
@patch('user_interface.controller.main_menu_controller.handle_menu_choice')
def run_menu_loop(mock_handle_menu_choice, mock_prompt_choice, mock_display_menu_with_title, mock_clear_screen, config):
    main_menu_controller.menu_loop(config)


# Shared Context
@given('the game is started')
def step_given_game_is_started(context):
    context.config = {}  # Mock configuration


@when('the main menu is displayed')
def step_when_main_menu_is_displayed(context):
    menu_options = {
        1: ("Start New Game", lambda config: print("Starting new game...")),
        2: ("Upload Sudoku", lambda config: print("Uploading Sudoku...")),
        3: ("Load Saved Game", lambda config: print("Loading saved game...")),
        4: ("Exit", None)
    }

    with patch('user_interface.controller.main_menu_controller.get_menu_options', return_value=menu_options):
        # Mock get_menu_choice to always return 1 (or any consistent value)
        with patch('user_interface.controller.main_menu_controller.get_menu_choice', return_value=1):
            run_menu_loop(config=context.config)


@then('the following options are shown:')
def step_then_options_are_shown(context):
    expected_menu = {
        1: "Start New Game",
        2: "Upload Sudoku",
        3: "Load Saved Game",
        4: "Exit"
    }

    with patch('user_interface.controller.main_menu_controller.get_menu_options', return_value=expected_menu):
        main_menu_controller.display_menu_with_title("Main Menu", expected_menu)

    for row in context.table:
        option_number = int(row['option'].split('.')[0])
        assert expected_menu[option_number] in row['option'], f"Expected option '{row['option']}' not found."


@when('the player selects a valid menu option')
def step_when_player_selects_valid_menu_option(context):
    context.selected_option = 1  # Simulating selection of "Start New Game"
    with patch('user_interface.controller.main_menu_controller.get_menu_choice', return_value=context.selected_option):
        run_menu_loop(config=context.config)


@then('the corresponding action is executed')
def step_then_corresponding_action_executed(context):
    actions = {
        1: "Starting new game...",
        2: "Uploading Sudoku...",
        3: "Loading saved game...",
        4: "Exiting the game..."
    }
    with patch('user_interface.controller.main_menu_controller.get_menu_options', return_value=actions):
        result = main_menu_controller.handle_menu_choice(context.config, context.selected_option, actions)
        expected_action_output = actions[context.selected_option]
        assert result == expected_action_output, f"Expected action '{expected_action_output}', but got '{result}'"


@when('the player selects an invalid menu option')
def step_when_player_selects_invalid_menu_option(context):
    context.selected_option = 5  # Simulating invalid option selection
    with patch('user_interface.controller.main_menu_controller.get_menu_choice', return_value=context.selected_option):
        run_menu_loop(config=context.config)


@then('an error message "Invalid choice. Please enter a valid number." is displayed')
def step_then_error_message_displayed(context):
    with patch('user_interface.controller.main_menu_controller.display_invalid_input') as mock_display_invalid_input:
        main_menu_controller.handle_menu_choice(context.config, context.selected_option, {})
        mock_display_invalid_input.assert_called_with("Invalid choice. Please enter a valid number.")


@given('the main menu is displayed')
def step_given_main_menu_is_displayed(context):
    step_when_main_menu_is_displayed(context)


@then('the main menu is displayed again')
def step_then_main_menu_is_displayed_again(context):
    step_when_main_menu_is_displayed(context)
