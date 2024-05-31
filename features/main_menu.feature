Feature: Display Main Menu Options
  As a player
  I want to see the main menu options
  So that I can navigate the game

  Scenario: Display the main menu
    Given the game is started
    When the main menu is displayed
    Then the following options are shown:
      | 1. Start New Game  |
      | 2. Upload Sudoku   |
      | 3. Load Saved Game |
      | 4. Exit            |

  Scenario: Player selects a valid menu option
    Given the main menu is displayed
    When the player selects a valid menu option
    Then the corresponding action is executed

  Scenario: Player selects an invalid menu option
    Given the main menu is displayed
    When the player selects an invalid menu option
    Then an error message "Invalid choice. Please enter a valid number." is displayed
    And the main menu is displayed again
