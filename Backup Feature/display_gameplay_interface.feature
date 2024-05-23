Feature: Gameplay Interface
  The gameplay interface displays the Sudoku grid and allows users to interact with the puzzle.

  Scenario: Display Sudoku grid
    Given a Sudoku puzzle is loaded (generated, uploaded, or resumed)
    Then the gameplay interface should display the Sudoku grid with pre-filled and empty cells


