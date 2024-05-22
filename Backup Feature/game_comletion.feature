Feature: Game Completion
  Users can request validation of their completed puzzle, and the system handles correct and incorrect solutions.

  Scenario: User requests solution validation
    Given the user has filled all cells in the Sudoku grid
    When the user requests to validate the solution
    Then the system should verify if all cells adhere to Sudoku rules throughout the grid

  Scenario: Correct solution
    Given the user's solution adheres to Sudoku rules
    When the system validates the solution
    Then it should display a congratulatory message indicating a correct solution

  Scenario: Incorrect solution
    Given the user's solution violates Sudoku rules
    When the system validates the solution
    Then it should display error notifications
    And message mentions the specific cells that violate the rules
    And offer options to highlight the errors on the grid or reveal the complete solution
