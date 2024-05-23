import sys
from io import StringIO

from behave import given, when, then

# Mock the functions to test their outputs
from user_interface.display.menu_display import display_main_menu, display_invalid_input


@given('the game application is launched')
def step_given_game_application_is_launched(context):
    # Redirect stdout to capture print statements
    context.stdout = StringIO()
    sys.stdout = context.stdout

    # Call the display_main_menu function to simulate launching the app
    display_main_menu()
    # Save the captured output
    context.main_menu_output = context.stdout.getvalue().strip().split('\n')
    sys.stdout = sys.__stdout__


@then('the system displays the main menu with options')
def step_then_system_displays_main_menu_with_options(context):
    # Use the saved captured output from context
    output = context.main_menu_output

    expected_menu = [
        "Main Menu:",
        "1. Start New Game",
        "2. Upload Sudoku",
        "3. Load Saved Game",
        "4. Exit"
    ]

    # Check if the output matches the expected menu options
    assert output == expected_menu, f"Expected: {expected_menu}, but got: {output}"


@given('the user is on the main menu')
def step_given_user_is_on_the_main_menu(context):
    # Redirect stdout to capture print statements
    context.stdout = StringIO()
    sys.stdout = context.stdout

    # Call the display_main_menu function to simulate the user being on the main menu
    display_main_menu()
    context.main_menu_output = context.stdout.getvalue().strip().split('\n')
    sys.stdout = sys.__stdout__


@when('the user enters an invalid command')
def step_when_user_enters_invalid_command(context):
    # Simulate entering an invalid command by capturing output again
    context.stdout = StringIO()
    sys.stdout = context.stdout
    display_invalid_input("Invalid input. Please enter a number between 1 and 4.")
    context.invalid_command_output = context.stdout.getvalue().strip().split('\n')
    sys.stdout = sys.__stdout__


@then('the system displays an error message "Invalid input. Please enter a number between 1 and 4."')
def step_then_system_displays_error_message(context):
    # Capture the output again
    output = context.invalid_command_output

    expected_error_message = [
        "Invalid input. Please enter a number between 1 and 4.",
        "Main Menu:",
        "1. Start New Game",
        "2. Upload Sudoku",
        "3. Load Saved Game",
        "4. Exit"
    ]

    # Check if the output matches the expected error message and menu options
    assert output == expected_error_message, f"Expected: {expected_error_message}, but got: {output}"


@then('re-displays the main menu with options')
def step_then_redisplays_main_menu_with_options(context):
    # This step is already covered in the previous step definition, so it can be left empty
    pass
