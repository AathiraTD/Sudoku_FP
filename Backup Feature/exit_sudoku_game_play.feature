Feature: Exit game during game play

  Scenario: User exits the game
    Given the user is on the gameplay interface
    When the user requests to exit the game
    Then the system should display a confirmation prompt
    And upon confirmation, exit the game or ignore the request