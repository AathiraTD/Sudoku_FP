import sys
from io import StringIO

from behave import given, when, then

from core_data.game_state import GameState
from puzzle_handler.generate.generate_puzzle import generate_puzzle
from user_interface.display.menu_display import display_main_menu, display_invalid_input


# Helper to capture output
def capture_output(func, *args, **kwargs):
    old_stdout = sys.stdout
    sys.stdout = captured_output = StringIO()
    try:
        func(*args, **kwargs)
        return captured_output.getvalue()
    finally:
        sys.stdout = old_stdout


@given('the user is on the gameplay interface')
def step_given_user_on_gameplay_interface(context):
    context.game_state = GameState(grid=generate_puzzle({"grid_size": 9}, "easy"), config={"hint_limit": 3})

@given('the user is on the main menu')
def step_given_user_on_main_menu(context):
    context.stdout = capture_output(display_main_menu)
    context.menu_output = context.stdout.split('\n')


@given('the game application is launched')
def step_given_game_application_is_launched(context):
    context.stdout = StringIO()
    sys.stdout = context.stdout
    display_main_menu()
    context.main_menu_output = context.stdout.getvalue().strip().split('\n')
    sys.stdout = sys.__stdout__


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
