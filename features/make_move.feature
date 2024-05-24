Feature: Make a Move in Sudoku
  As a Sudoku player
  I want to make moves on the Sudoku grid
  So that I can solve the puzzle

  Scenario: Making a valid move
    Given the game state is initialized
    When the user makes a valid move by filling an empty cell
    Then the move is applied to the grid
    And the move is pushed to the undo stack
    And the system displays a success message

  Scenario: Making an invalid move due to input format
    Given the game state is initialized
    When the user makes an invalid move by A1=XYZ
    Then the system displays an error message for invalid format

  Scenario: Making a move in a pre-filled cell
    Given the game state is initialized
    And the current grid has a pre-filled cell
    When the user makes a move
    Then the system displays an error message for pre-filled cell
