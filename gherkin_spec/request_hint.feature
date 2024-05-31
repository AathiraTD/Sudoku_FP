Feature: Request a hint

  Scenario: Successfully request a hint
    Given the user is playing a game
    And the user has not reached the hint limit
    When the user requests a hint
    Then the system asks if the hint is for a random cell or a specific cell
    When the user chooses a random cell
    Then a hint should be provided for a random empty cell
    And the hint count should be incremented

  Scenario: Successfully request a hint for a specific cell
    Given the user is playing a game
    And the user has not reached the hint limit
    When the user requests a hint
    Then the system asks if the hint is for a random cell or a specific cell
    When the user chooses a specific cell
    Then the system prompts the user to input the coordinates
    And if the specified cell is empty
    Then a hint should be provided for the specified empty cell
    And the hint count should be incremented
    And if the specified cell is not empty
    Then an error message should be displayed indicating the cell is not empty

  Scenario: Request a hint with no empty cells
    Given the user is playing a game
    And the user has not reached the hint limit
    When the user requests a hint
    Then an error message should be displayed indicating no hints are available

  Scenario: Request a hint after reaching the hint limit
    Given the user is playing a game
    And the user has reached the hint limit
    When the user requests a hint
    Then an error message should be displayed indicating no more hints are available
