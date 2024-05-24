Feature: Undo Moves

  Scenario: User undo the last move
    Given the user has made one or more moves on the Sudoku grid
    When the user selects the "Undo" option
    Then the system should revert the grid to the state before the last move

  Scenario: No more undo available
    Given the user has reverted all possible moves
    When the user attempts to undo a move
    Then the system should notify the user that no more moves from the user exist to undo