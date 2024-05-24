Feature: Save Game Functionality in Sudoku

  Scenario: User initiates game save
    Given the user is on the gameplay interface
    When the user requests to save the game
    Then the system saves the current game state (grid, filled cells, progress)
    And displays a confirmation message that the game has been saved