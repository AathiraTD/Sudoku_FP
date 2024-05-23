from behave import given, when, then
from unittest.mock import patch
from user_interface.main_menu import menu_loop
from user_interface.user_input import get_difficulty_choice
from puzzle_handler.generate.generate_puzzle import generate_puzzle, PuzzleGenerationError
from user_interface.display.display_grid import display_grid
from utils.validation_utils import validate_grid

# Global variables to store state across steps
grid_size = 9
selected_difficulty = None
selected_difficulty_level = None
generated_sudoku = None
invalid_difficulty_level = None

# Scenario: User selects "New Game" option
@given('the user is on the main menu')
def step_given_user_on_main_menu():
    global grid_size
    grid_size = 9  # Assuming a 9x9 grid size for the test
    print(f"Given: grid_size is {grid_size}")

@when('the user selects the "New Game" option')
def step_when_user_selects_new_game():
    with patch('builtins.input', return_value='1'):
        menu_loop({'grid_size': grid_size})
    print(f"When: grid_size is {grid_size}")

@then('the system should prompt the user to select a difficulty level')
def step_then_prompt_difficulty_level():
    with patch('builtins.input', return_value='1'):  # Simulating user selects "Easy"
        difficulty = get_difficulty_choice()
    assert difficulty in ["easy", "medium", "hard"]
    global selected_difficulty
    selected_difficulty = difficulty
    print(f"Then (prompt difficulty): difficulty is {difficulty}")

# Scenario: User selects a difficulty level for a new game
@given('the user has been prompted to select a difficulty level')
def step_given_prompted_difficulty_level():
    print("Given (prompted difficulty): user prompted to select difficulty level")

@when('the user selects a difficulty level (e.g., Easy, Medium, Hard)')
def step_when_user_selects_difficulty():
    with patch('builtins.input', return_value='1'):  # Simulating user selects "Easy"
        difficulty_level = get_difficulty_choice()
    global selected_difficulty_level
    selected_difficulty_level = difficulty_level
    print(f"When (select difficulty): selected difficulty level is {difficulty_level}")

@then('the system initiates the Sudoku puzzle generation process for the selected difficulty level')
def step_then_initiate_sudoku_generation():
    assert selected_difficulty_level == "easy"
    try:
        print(f"Then (initiate generation): grid_size before generation is {grid_size}")
        generated_puzzle = generate_puzzle({'grid_size': grid_size}, selected_difficulty_level)
    except PuzzleGenerationError:
        generated_puzzle = None
    assert generated_puzzle is not None
    global generated_sudoku
    generated_sudoku = generated_puzzle
    print("Then (initiate generation): Puzzle generation successful")

# Scenario: User starts a new game without selecting a difficulty level / invalid level
@when('the user does not select a difficulty level or selects an invalid level')
def step_when_user_does_not_select_difficulty():
    with patch('builtins.input', side_effect=['4', 'invalid', '']):
        try:
            invalid_level = get_difficulty_choice()
        except ValueError as e:
            invalid_level = str(e)
    global invalid_difficulty_level
    invalid_difficulty_level = invalid_level
    print(f"When (invalid difficulty): invalid level is {invalid_level}")

@then('the system displays a message prompting the user to input a valid difficulty level')
def step_then_prompt_valid_difficulty():
    assert "Invalid input" in invalid_difficulty_level or "Invalid choice" in invalid_difficulty_level
    print("Then (prompt valid difficulty): User prompted for valid difficulty")

# Scenario: System generates a valid Sudoku puzzle
@given('the system has initiated the Sudoku puzzle generation process')
def step_given_sudoku_generation_initiated():
    try:
        generated_puzzle = generate_puzzle({'grid_size': grid_size}, selected_difficulty_level)
    except PuzzleGenerationError:
        generated_puzzle = None
    global generated_sudoku
    generated_sudoku = generated_puzzle
    print("Given (generation initiated): Sudoku puzzle generation initiated")

@when('the system generates a Sudoku puzzle')
def step_when_generate_sudoku_puzzle():
    try:
        generated_puzzle = generate_puzzle({'grid_size': grid_size}, selected_difficulty_level)
    except PuzzleGenerationError:
        generated_puzzle = No
    assert generated_puzzle is not None
    global generated_sudoku
    generated_sudoku = generated_puzzle
    print("When (generate puzzle): Sudoku puzzle generated")

@then('the generated puzzle should have a unique solution')
def step_then_validate_puzzle_solution():
    assert validate_grid(generated_sudoku.rows, generated_sudoku.grid_size)
    print("Then (validate solution): Puzzle has a unique solution")

@then('the system should display the generated Sudoku grid on the gameplay interface')
def step_then_display_sudoku_grid():
    with patch('builtins.print') as mock_print:
        display_grid(generated_sudoku)
        mock_print.assert_called()
    print("Then (display grid): Sudoku grid displayed on interface")
