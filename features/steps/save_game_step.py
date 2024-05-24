import json
import os
from unittest.mock import patch

from behave import when, then

from features.steps.common_steps import capture_output
from user_actions.save_game import save_game_to_file, write_to_file, game_state_to_dict


@when('the user requests to save the game')
def step_when_user_requests_save_game(context):
    with patch('builtins.input', side_effect=['test_save.json', '1']):
        file_name, directory, game_state_dict = save_game_to_file(context.game_state)
        context.stdout = capture_output(write_to_file, file_name, directory, game_state_dict)
        context.save_output = context.stdout.split('\n')

@then('the system saves the current game state (grid, filled cells, progress)')
def step_then_saves_game_state(context):
    file_name = 'test_save.json'
    directory = os.getcwd()
    file_path = os.path.join(directory, file_name)

    assert os.path.exists(file_path), f"Expected save file to exist at {file_path}"

    with open(file_path, 'r') as file:
        saved_game_state = json.load(file)

    expected_game_state = game_state_to_dict(context.game_state)
    assert saved_game_state == expected_game_state, "The saved game state does not match the expected state"

@then('displays a confirmation message that the game has been saved')
def step_then_displays_confirmation_message(context):
    assert any("Game saved successfully" in line for line in context.save_output), \
        f"Expected confirmation message, but got: {context.save_output}"
