
Feature: User wants to input custom Sudoku by inserting it

  Scenario: User selects "Custom Sudoku" option
    Given the user is on the main menu
    When the user selects the "Custom Sudoku" option
    Then the system should prompt the user to input Sudoku values

  Scenario: User inputs a valid Sudoku puzzle
    Given the user has been prompted to input Sudoku values
    When the user enters a valid Sudoku puzzle
    Then the system validates the input
    And the validation is successful
    And the system displays a "Valid" message
    And displays the uploaded Sudoku grid on the gameplay interface

  Scenario: User inputs an invalid Sudoku puzzle
    Given the user has been prompted to input Sudoku values
    When the user enters an invalid Sudoku puzzle
    Then the system validates the input
    And the validation fails
    And the system displays a "Failure" message
    And provides specific details about the validation errors (e.g., "Invalid grid size", "Duplicate values in row/column/subgrid")

  Scenario: User inputs a valid Sudoku puzzle with multiple solutions
    Given the user has been prompted to input Sudoku values
    When the user enters a valid Sudoku puzzle with multiple solutions
    Then the system validates the input
    And the validation is successful
    And the system displays a "Valid" message
    And displays a error message that the puzzle has multiple solutions
    And displays the uploaded Sudoku grid on the gameplay interface
    And returns the user to the main menu