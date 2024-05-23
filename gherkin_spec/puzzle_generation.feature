Feature: Puzzle Generation
  The system generates Sudoku puzzles with varying difficulty levels and ensures unique solutions.

  Scenario: User selects a difficulty level
    Given the user has selected the "New Game" option
    When the user is prompted to choose a difficulty level
    Then the user should be able to select from available difficulty levels (e.g., Easy, Medium, Hard)

  Scenario: System generates a Sudoku puzzle with a unique solution
    Given the user has selected a difficulty level or chosen to start a new game
    When the system generates a Sudoku puzzle
    Then the generated puzzle should have a unique solution
    And the system should validate that the puzzle can be solved logically

  Scenario: System prevents puzzles with multiple solutions
    Given the user has selected a difficulty level or chosen to start a new game
    When the system generates a Sudoku puzzle
    Then the system should ensure the puzzle does not have multiple solutions
    And the system should validate the uniqueness of the solution
