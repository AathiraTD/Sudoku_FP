Feature: User input value in a cell to solve the Sudoku

  Scenario: User enters a value in an empty cell
    Given the user is on the gameplay interface
    When the user enters coordinates and a value for an empty cell
    Then the system should update the grid with the entered value
    And provide feedback on the move legality

  Scenario: User enters a valid move
    Given the user is on the gameplay interface
    And the cell is empty
    When the user enters a value that does not conflict with existing values in the same row, column, or subgrid
    Then the system updates the grid with the entered value
    And displays a message confirming the move is valid

  Scenario: User enters an invalid move
    Given the user is on the gameplay interface
    And the cell is empty
    When the user enters a value that conflicts with existing values in the same row, column, or subgrid
    Then the system does not update the grid with the entered value
    And displays an error message indicating the move is invalid

  Scenario: User attempts to enter a value in a pre-filled cell
    Given the user is on the gameplay interface
    And the cell is pre-filled
    When the user attempts to enter a value in the pre-filled cell
    Then the system does not allow the value to be entered
    And displays an error message indicating the cell cannot be modified