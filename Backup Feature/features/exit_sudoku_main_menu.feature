Feature: Exit game

  Scenario: User selects "Exit" option
    Given the user is on the main menu
    When the user selects the "Exit" option
    Then the game application should close