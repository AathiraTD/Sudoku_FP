Feature: Display Main Menu
  The main menu provides options to start a new game, upload a Sudoku puzzle, resume a saved game, or exit the application.

  Scenario: Display The Main Menu
    Given the game application is launched
    Then the system displays the main menu with options
        | Option              |
        | "1. Start New Game"  |
        | "2. Upload Sudoku"   |
        | "3. Load Saved Game" |
        | "4. Exit"            |

  Scenario: User inputs an invalid command
    Given the user is on the main menu
    When the user enters an invalid command
    Then the system displays an error message "Invalid input. Please enter a number between 1 and 4."
    And re-displays the main menu with options:
        | Option              |
        | "1. Start New Game"  |
        | "2. Upload Sudoku"   |
        | "3. Load Saved Game" |
        | "4. Exit"            |






