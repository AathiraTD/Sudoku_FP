Feature: Save Game Functionality in Sudoku

  Scenario: User initiates game save
    Given the user is on the gameplay interface
    When the user requests to save the game
    Then the system should prompt the user to choose a filename

  Scenario: User provides a valid filename
    Given the user is prompted to choose a filename
    When the user enters a valid filename
    Then the system saves the current game state (grid, filled cells, progress)
    And displays a confirmation message that the game has been saved
    And returns to the main menu

  Scenario: User provides an invalid filename
    Given the user is prompted to choose a filename
    When the user enters an invalid filename (e.g. empty)
    Then the system displays an error message indicating the filename is invalid
    And prompts the user to enter a valid filename

  Scenario: User cancels the save operation
    Given the user is prompted to choose a filename
    When the user cancels the save operation
    Then the system does not save the game
    And returns to the gameplay interface

  Scenario: User provides a duplicate filename
    Given the user is prompted to choose a filename
    And a file with the same name already exists in the directory
    When the user enters a filename that matches an existing file
    Then the system displays an error message indicating the file name is already in use
    And prompts the user to enter a different filename
