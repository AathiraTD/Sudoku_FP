import os
import sys
from io import StringIO
from unittest.mock import patch

from behave import given, when, then

# Assuming the following functions are imported from their respective modules
from user_actions.load_saved_game import (
    list_saved_game_files,
    prompt_for_file_choice,
    load_saved_game
)


# Helper to capture output
def capture_output(func, *args, **kwargs):
    old_stdout = sys.stdout
    sys.stdout = captured_output = StringIO()
    try:
        func(*args, **kwargs)
        return captured_output.getvalue()
    finally:
        sys.stdout = old_stdout


@when('the user selects the "Load Saved Sudoku" option')
def step_when_user_selects_load_saved_sudoku(context):
    with patch('builtins.input', side_effect=['1']):
        with patch('os.listdir', return_value=['save1.json', 'save2.json']):
            with patch('user_actions.load_saved_game.load_saved_game', return_value="Loading saved game data..."):
                context.stdout = capture_output(load_saved_game, config={})
                context.load_output = context.stdout.split('\n')


@then('the system displays a list of available saved games (if any)')
def step_then_displays_list_of_saved_games(context):
    with patch('os.listdir', return_value=['save1.json', 'save2.json']):
        directory = os.getcwd()
        context.saved_games = list_saved_game_files(directory)
        assert 'save1.json' in context.saved_games
        assert 'save2.json' in context.saved_games


@then('prompts the user to specify the file to load')
def step_then_prompts_for_file_to_load(context):
    assert any("Enter the number of the file to load:" in line for line in context.load_output), \
        f"Expected prompt for file name, but got: {context.load_output}"


@given('the user has been prompted to specify a saved game file')
def step_given_user_prompted_for_saved_game_file(context):
    context.saved_game_files = ['save1.json', 'save2.json']
    context.stdout = capture_output(prompt_for_file_choice, context.saved_game_files)
    context.prompt_output = context.stdout.split('\n')


@when('the user selects a saved game file')
def step_when_user_selects_saved_game_file(context):
    with patch('builtins.input', return_value='1'):
        context.chosen_file = capture_output(prompt_for_file_choice, context.saved_game_files).strip()
        context.file_path = os.path.join(os.getcwd(), context.chosen_file)
        with patch('user_actions.load_saved_game.load_saved_game', return_value="Loading saved game data..."):
            context.stdout = capture_output(load_saved_game, config={}, file_path=context.file_path)
            context.load_output = context.stdout.split('\n')


@then('the system validates the selected file format and data integrity')
def step_then_validates_file_format_and_data_integrity(context):
    with patch('user_actions.load_saved_game.validate_saved_game_file', return_value=True):
        assert any("Validating file format and data integrity..." in line for line in context.load_output), \
            f"Expected validation message, but got: {context.load_output}"


@then('the validation is successful')
def step_then_validation_is_successful(context):
    assert any("Validation successful." in line for line in context.load_output), \
        f"Expected validation success message, but got: {context.load_output}"


@then('the system loads the saved game data')
def step_then_loads_saved_game_data(context):
    assert any("Loading saved game data..." in line for line in context.load_output), \
        f"Expected loading message, but got: {context.load_output}"


@then('displays the Sudoku grid with pre-filled and empty cells on the gameplay interface')
def step_then_displays_sudoku_grid(context):
    with patch('user_interface.main_handler.display_main_menu', return_value="Displaying Sudoku grid..."):
        assert any("Displaying Sudoku grid:" in line for line in context.load_output), \
            f"Expected grid display message, but got: {context.load_output}"
