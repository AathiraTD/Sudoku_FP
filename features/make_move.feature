Feature: Make a Move in Sudoku
  As a Sudoku player
  I want to make moves on the Sudoku grid
  So that I can solve the puzzle

  Scenario: Making a valid move
    Given the game state is initialized
    When the user makes a valid move "A1=5"
    Then the move is applied to the grid
    And the move is pushed to the undo stack
    And the system displays "Move A1=5 applied successfully."

  Scenario: Making an invalid move due to format
    Given the game state is initialized
    When the user makes an invalid move "A1=XYZ"
    Then the system displays "Error: Invalid input format."

  Scenario: Making an invalid move due to Sudoku rules
    Given the game state is initialized
    And the current grid has a 5 in cell "A1"
    When the user makes a move "A2=5"
    Then the system displays "Invalid move at A2. Does not satisfy Sudoku rules."

  Scenario: Making a move in a pre-filled cell
    Given the game state is initialized
    And the current grid has a pre-filled cell at "A1"
    When the user makes a move "A1=6"
    Then the system displays "Cannot apply move A1=6. The cell is pre-filled or a hint."

