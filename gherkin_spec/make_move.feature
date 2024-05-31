Feature: Make a move

  Scenario: Successfully make a valid move
    Given the user is playing a game
    When the user makes a move in an empty cell with a valid number
    Then the cell should be updated with the new number

  Scenario: Attempt to make an invalid move
    Given the user is playing a game
    When the user makes a move in an empty cell with an invalid number
    Then an error message should be displayed
