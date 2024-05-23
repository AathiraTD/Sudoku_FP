Feature: Display Main Menu
  The main menu provides options to start a new game, upload a Sudoku puzzle, resume a saved game, or exit the application.

  Scenario: Display Main Menu
    Given the game application is launched
    Then the system displays the main menu with options:
        | Option              |
        | "New Game"          |
        | "Upload Sudoku"     |
        | "Resume Saved Game" |
        | "Exit"              |

  Scenario: User inputs an invalid command
    Given the user is on the main menu
    When the user enters an invalid command
    Then the system displays an error message "Invalid option. Please select a valid menu option."
    And re-displays the main menu with options:
        | Option              |
        | "New Game"          |
        | "Upload Sudoku"     |
        | "Resume Saved Game" |
        | "Exit"              |






