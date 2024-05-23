Feature: Sudoku Hint System

  Scenario: User requests a hint for an empty cell
    Given the user is on the gameplay interface
    And there are empty cells in the grid
    When the user requests a hint for a specific empty cell
    Then the system analyzes the puzzle state
    And suggests possible numbers that can be placed in the selected cell
    And highlights the suggested cell on the grid

  Scenario: User requests a general hint
    Given the user is on the gameplay interface
    And there are multiple empty cells in the grid
    When the user requests a general hint
    Then the system analyzes the puzzle state
    And suggests a strategic move or provides guidance on solving a specific row, column, or subgrid
    And highlights the area on the grid where the hint applies

  Scenario: User requests a hint but the puzzle is already complete
    Given the user is on the gameplay interface
    And the Sudoku puzzle is fully completed
    When the user requests a hint
    Then the system indicates that the puzzle is already complete
    And no further hints are necessary
    And displays a message suggesting the user to verify the solution

  Scenario: User requests a hint with only one solution possibility left
    Given the user is on the gameplay interface
    And there is only one possible solution for the remaining cells
    When the user requests a hint
    Then the system analyzes the puzzle state
    And suggests the number for the specific remaining cell(s)
    And highlights the cell(s) on the grid
