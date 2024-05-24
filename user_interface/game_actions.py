from core_data.game_state import GameState
from user_actions.make_a_move import make_a_move
from user_actions.request_hint import request_hint
from user_actions.save_game import save_game_to_file  # Import the save game function
from user_actions.undo_move import undo_move


def game_actions(game_state: GameState) -> None:
    """
    Function to handle game actions.

    Args:
        game_state (GameState): The current state of the game.
    """

    def display_menu() -> None:
        """
        Display the game actions menu.
        """
        print("\nChoose an action:")
        print("1. Make a move")
        print("2. Get a hint")
        print("3. Undo last move")
        # print("4. Redo last move")
        print("4. Solve the puzzle")
        print("5. Save the game")
        print("6. Back to main menu")

    def handle_action(choice: int, game_state: GameState) -> GameState:
        """
        Handle the user's action choice.

        Args:
            choice (int): The user's action choice.
            game_state (GameState): The current state of the game.

        Returns:
            GameState: The updated state of the game.
        """
        if choice == 1:
            game_state = make_a_move(game_state)  # Handle making a move
        elif choice == 2:
            game_state = request_hint(game_state)  # Handle requesting a hint
        elif choice == 3:
            game_state = undo_move(game_state)  # Handle undo last move
        # elif choice == 4:
        #     game_state = redo_move(game_state)  # Handle redo last move
        elif choice == 4:
            from user_actions.solve_puzzle import solve_puzzle  # Local import to avoid circular dependency
            game_state = game_state.with_grid(solve_puzzle(game_state.grid))  # Handle solving the puzzle
        elif choice == 5:
            save_game_to_file(game_state)  # Handle saving the game
        return game_state

    def prompt_action() -> int:
        """
        Recursively prompt the user for a valid action choice.

        Returns:
            int: The user's valid action choice.
        """
        try:
            choice = int(input("> "))  # Get input from the user
            if 1 <= choice <= 6:
                return choice  # Return valid choice
            else:
                print("Invalid choice. Please enter a number between 1 and 7.")
                return prompt_action()  # Recursive call for invalid input
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 6.")
            return prompt_action()  # Recursive call for non-integer input

    def game_loop(game_state: GameState) -> None:
        """
        Recursively handle the game loop.

        Args:
            game_state (GameState): The current state of the game.
        """
        display_menu()  # Display the game actions menu
        choice = prompt_action()  # Get the user's action choice
        if choice == 6:
            return  # Exit the loop to return to the main menu
        new_game_state = handle_action(choice, game_state)  # Handle the user's action choice
        game_loop(new_game_state)  # Recursive call with the updated game state

    game_loop(game_state)  # Initial call to start the game loop
