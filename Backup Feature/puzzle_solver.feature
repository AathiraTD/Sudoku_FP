Feature: System Solving Sudoku
  The system can analyze a puzzle and generate the solution, displaying the completed grid and main menu options.

  Scenario: User requests system to solve the Sudoku puzzle
    Given the user has a valid Sudoku grid
    When the user requests the system to solve the puzzle
    Then the system should analyze the puzzle and generate the solution
    And display the completed grid
    And show a clear message indicating the puzzle is solved
    And display the main menu options

  Scenario: Displaying completed grid
    Given the system has generated the solution
    When the solution is ready
    Then it should display the completed Sudoku grid
    And provide a message stating "Puzzle Solved!"
    And offer the main menu options
