from core_data.grid.grid import Grid
from puzzle_handler.solve.solve_puzzle import solve_puzzle
from user_actions.request_hint import request_hint
from user_actions.make_a_move import make_a_move
from user_actions.save_game import save_game_to_file  # Import the save game function

def game_actions(config: dict, grid: Grid) -> None:
    """
    Function to handle game actions.

    Args:
        config (dict): Configuration settings.
        grid (Grid): The current state of the Sudoku grid.
    """

    def display_menu() -> None:
        """
        Display the game actions menu.
        """
        print("\nChoose an action:")
        print("1. Make a move")
        print("2. Get a hint")
        print("3. Undo last move")
        print("4. Redo last move")
        print("5. Solve the puzzle")
        print("6. Save the game")
        print("7. Back to main menu")

    def handle_action(choice: int, grid: Grid) -> Grid:
        """
        Handle the user's action choice.

        Args:
            choice (int): The user's action choice.
            grid (Grid): The current state of the Sudoku grid.

        Returns:
            Grid: The updated state of the Sudoku grid.
        """
        if choice == 1:
            grid = make_a_move(grid)  # Handle making a move
        elif choice == 2:
            grid = request_hint(grid)  # Handle requesting a hint
        elif choice == 3:
            # Placeholder for undo last move
            print("Undo last move is not implemented yet.")
        elif choice == 4:
            # Placeholder for redo last move
            print("Redo last move is not implemented yet.")
        elif choice == 5:
            grid = solve_puzzle(grid)  # Handle solving the puzzle
        elif choice == 6:
            save_game_to_file(grid)  # Handle saving the game
        return grid

    def prompt_action() -> int:
        """
        Recursively prompt the user for a valid action choice.

        Returns:
            int: The user's valid action choice.
        """
        try:
            choice = int(input("> "))  # Get input from the user
            if 1 <= choice <= 7:
                return choice  # Return valid choice
            else:
                print("Invalid choice. Please enter a number between 1 and 7.")
                return prompt_action()  # Recursive call for invalid input
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 7.")
            return prompt_action()  # Recursive call for non-integer input

    while True:
        display_menu()  # Display the game actions menu
        choice = prompt_action()  # Get the user's action choice
        if choice == 7:
            break  # Exit the loop to return to the main menu
        grid = handle_action(choice, grid)  # Handle the user's action choice
