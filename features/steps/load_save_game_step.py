import os
from unittest.mock import patch

from behave import when, then
from pytest_bdd import given

from features.steps.common_steps import capture_output, step_given_user_on_main_menu
from user_actions.load_saved_game import list_saved_game_files, prompt_for_file_choice, load_saved_game


# Import the common step without redefining it
@given('the user is on the main menu')
def given_user_is_on_main_menu(context):
    step_given_user_on_main_menu(context)


@when('the user selects the "Load Saved Sudoku" option')
def step_when_user_selects_load_saved_sudoku(context):
    with patch('builtins.input', return_value='3'):
        context.stdout = capture_output(load_saved_game, {})
        context.load_output = context.stdout.split('\n')


@then('the system displays a list of available saved games (if any)')
def step_then_displays_list_of_saved_games(context):
    with patch('os.listdir', return_value=['save1.json', 'save2.json']):
        context.stdout = capture_output(list_saved_game_files, os.getcwd())
        context.load_output = context.stdout.split('\n')
        assert 'save1.json' in context.load_output
        assert 'save2.json' in context.load_output


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
        context.stdout = capture_output(load_saved_game, context.file_path)
        context.load_output = context.stdout.split('\n')


@then('the system validates the selected file format and data integrity')
def step_then_validates_file_format_and_data_integrity(context):
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
    assert any("Displaying Sudoku grid:" in line for line in context.load_output), \
        f"Expected grid display message, but got: {context.load_output}"
