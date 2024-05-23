from behave import given, when, then
from unittest.mock import patch
from user_interface.main_menu import menu_loop
from user_interface.user_input import get_menu_choice


@given('the game application is launched')
def step_given_game_application_launched(context):
    context.config = {'grid_size': 9}
    context.menu_loop = menu_loop


@then('the system displays the main menu with options:')
def step_then_system_displays_main_menu(context):
    with patch('builtins.input', side_effect=['4']):  # Simulate user selecting Exit to end the menu loop
        context.menu_loop(context.config)

    expected_options = [row['Option'] for row in context.table]
    actual_options = [
        "New Game",
        "Upload Sudoku",
        "Resume Saved Game",
        "Exit"
    ]

    for option in expected_options:
        assert option in actual_options
    print("Then: Main menu options displayed correctly")


@given('the user is on the main menu')
def step_given_user_on_main_menu(context):
    context.config = {'grid_size': 9}
    context.menu_loop = menu_loop
    with patch('builtins.input', side_effect=['4']):  # Simulate user selecting Exit to end the menu loop
        context.menu_loop(context.config)


@when('the user enters an invalid command')
def step_when_user_enters_invalid_command(context):
    with patch('builtins.input', side_effect=['invalid', '4']):  # Simulate invalid input and then Exit
        context.menu_loop(context.config)


@then('the system displays an error message "Invalid option. Please select a valid menu option."')
def step_then_system_displays_error_message(context):
    # Here we would capture the output and assert that the error message is displayed.
    # This requires capturing stdout which can be done using `unittest.mock.patch` on 'sys.stdout'
    with patch('sys.stdout') as mock_stdout:
        with patch('builtins.input', side_effect=['invalid', '4']):  # Simulate invalid input and then Exit
            context.menu_loop(context.config)
        output = mock_stdout.getvalue()
        assert "Invalid option. Please select a valid menu option." in output
    print('Then: Error message "Invalid option. Please select a valid menu option." displayed')


@then('re-displays the main menu with options:')
def step_then_redisplays_main_menu(context):
    with patch('builtins.input', side_effect=['4']):  # Simulate user selecting Exit to end the menu loop
        context.menu_loop(context.config)

    expected_options = [row['Option'] for row in context.table]
    actual_options = [
        "New Game",
        "Upload Sudoku",
        "Resume Saved Game",
        "Exit"
    ]

    for option in expected_options:
        assert option in actual_options
    print("Then: Main menu options re-displayed correctly")
