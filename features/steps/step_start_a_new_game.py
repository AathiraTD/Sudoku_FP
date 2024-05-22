from behave import given, when, then
from unittest.mock import patch
from user_interface.main_menu import menu_loop
from user_interface.user_input import get_menu_choice, get_difficulty_choice
from puzzle_handler.generate.generate_puzzle import generate_puzzle, PuzzleGenerationError
from user_interface.display.display_grid import display_grid
from utils.validation_utils import validate_grid


# Scenario: User selects "New Game" option
# @given('the user is on the main menu')
# def step_given_user_on_main_menu(context):
#     if not hasattr(context, 'config'):
#         context.config = {}  # Initialize config if it doesn't exist
#     context.config['grid_size'] = 9  # Assuming a 9x9 grid size
#     context.menu_loop = menu_loop  # Reference to the menu loop function
#     print(f"Given: config is {context.config}")



# @when('the user selects the "New Game" option')
# def step_when_user_selects_new_game(context):
#     with patch('builtins.input', return_value='1'):
#         context.menu_loop(context.config)
#     print(f"When: config is {context.config}")
#

@then('the system should prompt the user to select a difficulty level')
def step_then_prompt_difficulty_level(context):
    with patch('builtins.input', return_value='1'):  # Simulating user selects "Easy"
        difficulty = get_difficulty_choice()
    assert difficulty in ["easy", "medium", "hard"]
    print(f"Then (prompt difficulty): difficulty is {difficulty}")


# Scenario: User selects a difficulty level for a new game
@given('the user has been prompted to select a difficulty level')
def step_given_prompted_difficulty_level(context):
    context.difficulty_prompt = get_difficulty_choice
    print("Given (prompted difficulty): user prompted to select difficulty level")


@when('the user selects a difficulty level (e.g., Easy, Medium, Hard)')
def step_when_user_selects_difficulty(context):
    with patch('builtins.input', return_value='1'):  # Simulating user selects "Easy"
        context.difficulty_level = context.difficulty_prompt()
    print(f"When (select difficulty): selected difficulty level is {context.difficulty_level}")


@then('the system initiates the Sudoku puzzle generation process for the selected difficulty level')
def step_then_initiate_sudoku_generation(context):
    assert context.difficulty_level == "easy"
    try:
        print(f"Then (initiate generation): config before generation is {context.config}")
        context.generated_puzzle = generate_puzzle(context.config, context.difficulty_level)
    except PuzzleGenerationError:
        context.generated_puzzle = None
    assert context.generated_puzzle is not None
    print("Then (initiate generation): Puzzle generation successful")


# Scenario: User starts a new game without selecting a difficulty level / invalid level
@when('the user does not select a difficulty level or selects an invalid level')
def step_when_user_does_not_select_difficulty(context):
    with patch('builtins.input', side_effect=['4', 'invalid', '']):
        try:
            context.invalid_level = context.difficulty_prompt()
        except ValueError as e:
            context.invalid_level = str(e)
    print(f"When (invalid difficulty): invalid level is {context.invalid_level}")


@then('the system displays a message prompting the user to input a valid difficulty level')
def step_then_prompt_valid_difficulty(context):
    assert "Invalid input" in context.invalid_level or "Invalid choice" in context.invalid_level
    print("Then (prompt valid difficulty): User prompted for valid difficulty")


# Scenario: System generates a valid Sudoku puzzle
@given('the system has initiated the Sudoku puzzle generation process')
def step_given_sudoku_generation_initiated(context):
    context.difficulty_level = "easy"
    try:
        context.generated_puzzle = generate_puzzle(context.config, context.difficulty_level)
    except PuzzleGenerationError:
        context.generated_puzzle = None
    print("Given (generation initiated): Sudoku puzzle generation initiated")

#
# @when('the system generates a Sudoku puzzle')
# def step_when_generate_sudoku_puzzle(context):
#     try:
#         context.generated_puzzle = generate_puzzle(context.config, context.difficulty_level)
#     except PuzzleGenerationError:
#         context.generated_puzzle = None
#     assert context.generated_puzzle is not None
#     print("When (generate puzzle): Sudoku puzzle generated")
#
#
# @then('the generated puzzle should have a unique solution')
# def step_then_validate_puzzle_solution(context):
#     assert validate_grid(context.generated_puzzle.cells, context.generated_puzzle.grid_size)
#     print("Then (validate solution): Puzzle has a unique solution")
#
#
# @then('the system should display the generated Sudoku grid on the gameplay interface')
# def step_then_display_sudoku_grid(context):
#     # Assuming display_grid function prints the grid, we capture the print output
#     with patch('builtins.print') as mock_print:
#         display_grid(context.generated_puzzle)
#         mock_print.assert_called()
#     print("Then (display grid): Sudoku grid displayed on interface")
