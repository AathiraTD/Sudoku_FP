Feature: User want to play a new Game after loading the game

  Scenario: User selects "Start a New Game" option
    Given the user is on the main menu
    When the user selects the "Start a New Game" option
    Then the system should prompt the user to input a difficulty level

  Scenario: User selects a difficulty level for a new game
    Given the user has been prompted to select a difficulty level
    When the user selects a difficulty level (e.g., Easy, Medium, Hard)
    Then the system initiates the Sudoku puzzle generation process for the selected difficulty level

  Scenario: User starts a new game without selecting a difficulty level / invalid level
    Given the user has been prompted to select a difficulty level
    When the user does not select a difficulty level or selects an invalid level
    Then the system displays a message prompting the user to input a valid difficulty level

  Scenario: System generates a valid Sudoku puzzle
    Given the system has initiated the Sudoku puzzle generation process
    When the system generates a Sudoku puzzle
    Then the generated puzzle should have a unique solution
    And the system should display the generated Sudoku grid on the gameplay interface
    And the game play menu options are displayed for the user to play the game