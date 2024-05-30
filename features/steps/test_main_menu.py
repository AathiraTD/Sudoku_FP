from unittest.mock import patch

from behave import when, then

from features.steps.common_steps import capture_output
from user_interface.menu_display import display_main_menu


# When step for user selecting the main menu option
@when('the user selects the main menu option {option:d}')
def step_when_user_selects_main_menu_option(context, option):
    with patch('builtins.input', side_effect=[str(option)]):
        context.stdout = capture_output(display_main_menu)
        context.menu_output = context.stdout.split('\n')


# Then steps to verify the output
# Then steps to verify the output
@then('the system displays the main menu')
def step_then_displays_main_menu(context):
    assert any("Main Menu" in line for line in context.menu_output), \
        f"Expected main menu display, but got: {context.menu_output}"


@then('the system should navigate to the {destination}')
def step_then_navigate_to_destination(context, destination):
    expected_message = f"Navigating to {destination}"
    assert any(expected_message in line for line in context.menu_output), \
        f"Expected message containing '{expected_message}', but got: {context.menu_output}"
