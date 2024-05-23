Feature: Undo and Redo Moves

  Scenario: User undoes the last move
    Given the user has made one or more moves on the Sudoku grid
    When the user selects the "Undo" option
    Then the system should revert the grid to the state before the last move

  Scenario: User redoes the last undone move
    Given the user has undone one or more moves
    When the user selects the "Redo" option
    Then the system should reapply the last undone move to the grid

  Scenario: No more undos available
    Given the user has reverted all possible moves
    When the user attempts to undo a move
    Then the system should notify the user that no more undos are available

  Scenario: No more redos available
    Given the user has reapplied all possible undone moves
    When the user attempts to redo a move
    Then the system should notify the user that no more redos are available