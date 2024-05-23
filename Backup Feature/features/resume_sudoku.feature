Feature: Resume saved Sudoku

  Scenario: User selects "Resume Saved Sudoku" option
    Given the user is on the main menu
    When the user selects the "Resume Saved Sudoku" option
    Then the system displays a list of available saved games (if any)
    And prompts the user to specify the file to load

  Scenario: User selects a valid saved game file
    Given the user has been prompted to specify a saved game file
    When the user selects a saved game file
    Then the system validates the selected file format and data integrity
    And the validation is successful
    Then the system loads the saved game data
    And displays the Sudoku grid with pre-filled and empty cells on the gameplay interface

  Scenario: User selects an invalid or corrupted saved game file
    Given the user has been prompted to specify a saved game file
    When the user selects a saved game file
    Then the system validates the selected file format and data integrity
    And the validation fails
    Then the system displays an informative error message such as "Invalid file format" or "Corrupted save data"