import sys
from io import StringIO

from behave import given, when, then

from puzzle_handler.generate.generate_puzzle import generate_puzzle
from user_interface.display.display_grid import display_grid
from user_interface.menu_display import display_difficulty_options, display_invalid_input


@given('the user has been prompted to select a difficulty level')
def step_given_prompted_to_select_difficulty(context):
    context.stdout = StringIO()
    sys.stdout = context.stdout
    display_difficulty_options()
    context.difficulty_prompt_output = context.stdout.getvalue().strip().split('\n')
    sys.stdout = sys.__stdout__

@when('the user selects the "Start a New Game" option')
def step_when_user_selects_start_new_game_option(context):
    context.stdout = StringIO()
    sys.stdout = context.stdout
    display_difficulty_options()
    context.difficulty_prompt_output = context.stdout.getvalue().strip().split('\n')
    sys.stdout = sys.__stdout__

@then('the system should prompt the user to input a difficulty level')
def step_then_system_prompts_for_difficulty_level(context):
    output = context.difficulty_prompt_output
    expected_prompt = [
        "Choose difficulty level:",
        "1. Easy",
        "2. Medium",
        "3. Hard"
    ]
    assert output == expected_prompt, f"Expected: {expected_prompt}, but got: {output}"

@when('the user selects a difficulty level (e.g., Easy, Medium, Hard)')
def step_when_user_selects_difficulty_level(context):
    context.difficulty = "easy"  # You can extend this to choose randomly or based on test parameter
    context.stdout = StringIO()
    sys.stdout = context.stdout
    config = {"grid_size": 9}
    grid = generate_puzzle(config, context.difficulty)
    context.grid = grid
    context.puzzle_generation_output = context.stdout.getvalue().strip().split('\n')
    sys.stdout = sys.__stdout__

@then('the system initiates the Sudoku puzzle generation process for the selected difficulty level')
def step_then_initiates_sudoku_generation(context):
    assert context.grid is not None, "Failed to generate Sudoku puzzle"

@when('the user does not select a difficulty level or selects an invalid level')
def step_when_user_does_not_select_valid_difficulty(context):
    context.stdout = StringIO()
    sys.stdout = context.stdout
    display_invalid_input("Invalid input. Please enter a number between 1 and 3.")
    context.invalid_input_output = context.stdout.getvalue().strip().split('\n')
    sys.stdout = sys.__stdout__

@then('the system displays a message prompting the user to input a valid difficulty level')
def step_then_prompt_valid_difficulty_level(context):
    output = context.invalid_input_output
    expected_message = "Invalid input. Please enter a number between 1 and 3."
    assert expected_message in output, f"Expected message: {expected_message}, but got: {output}"

@given('the system has initiated the Sudoku puzzle generation process')
def step_given_initiated_sudoku_generation(context):
    config = {"grid_size": 9}
    context.grid = generate_puzzle(config, "hard")

@when('the system generates a Sudoku puzzle')
def step_when_generates_sudoku_puzzle(context):
    assert context.grid is not None, "Failed to generate Sudoku puzzle"
    context.stdout = StringIO()
    sys.stdout = context.stdout
    display_grid(context.grid)
    context.grid_display_output = context.stdout.getvalue().strip().split('\n')
    sys.stdout = sys.__stdout__

@then('the generated puzzle should have a unique solution')
def step_then_unique_solution(context):
    # Placeholder for unique solution verification logic
    pass

@then('the system should display the generated Sudoku grid on the gameplay interface')
def step_then_display_generated_grid(context):
    output = context.grid_display_output
    assert len(output) > 0, "Failed to display the Sudoku grid"

@then('the game play menu options are displayed for the user to play the game')
def step_then_display_game_play_menu(context):
    # Placeholder for gameplay menu options verification
    pass
