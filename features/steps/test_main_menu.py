import sys
from io import StringIO

from behave import when, then

from user_interface.display.menu_display import display_invalid_input


@then('the system displays the main menu with options')
def step_then_system_displays_main_menu_with_options(context):
    output = context.main_menu_output
    expected_menu = [
        "Main Menu:",
        "1. Start New Game",
        "2. Upload Sudoku",
        "3. Load Saved Game",
        "4. Exit"
    ]
    assert output == expected_menu, f"Expected: {expected_menu}, but got: {output}"

@when('the user enters an invalid command')
def step_when_user_enters_invalid_command(context):
    context.stdout = StringIO()
    sys.stdout = context.stdout
    display_invalid_input("Invalid input. Please enter a number between 1 and 4.")
    context.invalid_command_output = context.stdout.getvalue().strip().split('\n')
    sys.stdout = sys.__stdout__

@then('the system displays an error message "Invalid input. Please enter a number between 1 and 4."')
def step_then_system_displays_error_message(context):
    output = context.invalid_command_output
    expected_error_message = "Invalid input. Please enter a number between 1 and 4."
    assert expected_error_message in output, f"Expected message: {expected_error_message}, but got: {output}"


@then('re-displays the main menu with options')
def step_then_redisplays_main_menu_with_options(context):
    output = context.invalid_command_output
    expected_menu = [
        "Invalid input. Please enter a number between 1 and 4.",
        "Main Menu:",
        "1. Start New Game",
        "2. Upload Sudoku",
        "3. Load Saved Game",
        "4. Exit"
    ]
    assert output == expected_menu, f"Expected: {expected_menu}, but got: {output}"
