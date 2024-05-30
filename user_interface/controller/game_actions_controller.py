from core_data.game_state import GameState
from user_interface.display.menu_display import display_invalid_input, display_menu_with_title
from user_interface.input.menu_enums import get_menu_options, GameAction


def game_actions(game_state: GameState) -> None:
    """
    Function to handle game actions.

    Args:
        game_state (GameState): The current state of the game.
    """
    actions = get_menu_options(GameAction)
    game_actions_recursive(game_state, actions)


def game_actions_recursive(game_state: GameState, actions: dict) -> None:
    """
    Recursively handle game actions.

    Args:
        game_state (GameState): The current state of the game.
        actions (dict): Dictionary mapping choices to their handlers.
    """
    # Display the game action menu
    display_menu_with_title("Choose a Game Action", actions)
    # Prompt the user for their choice
    choice = prompt_action(len(actions))

    # Handle the chosen action and get the updated game state
    new_game_state = handle_action(choice, game_state, actions)
    # Continue recursion only if not returning to the main menu
    if new_game_state is not None:
        game_actions_recursive(new_game_state, actions)


def handle_action(choice: int, game_state: GameState, actions: dict) -> GameState:
    """
    Handle the user's action choice.

    Args:
        choice (int): The user's action choice.
        game_state (GameState): The current state of the game.
        actions (dict): Dictionary mapping choices to their handlers.

    Returns:
        GameState: The updated state of the game or None if returning to main menu.
    """
    action = actions.get(choice)
    if action:
        _, handler = action
        if handler:
            # Execute the handler function and return the updated game state
            return handler(game_state)
        else:
            # Handle "Back to main menu"
            print("Exiting to the main menu...")
            return None
    print("Invalid choice. Please enter a valid number.")
    return game_state


def prompt_action(num_options: int) -> int:
    """
    Prompt the user for a valid action choice.

    Args:
        num_options (int): The number of available options.

    Returns:
        int: The user's valid action choice.
    """
    choice = input("> ")
    if choice.isdigit() and 1 <= int(choice) <= num_options:
        return int(choice)
    else:
        display_invalid_input(f"Invalid choice. Please enter a number between 1 and {num_options}.")
        return prompt_action(num_options)
