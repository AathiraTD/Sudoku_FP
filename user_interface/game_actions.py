from core_data.game_state import GameState
from user_interface.display_utilities import display_invalid_input
from user_interface.menu_options import get_game_actions


def game_actions(game_state: GameState) -> None:
    """
    Function to handle game actions.

    Args:
        game_state (GameState): The current state of the game.
    """
    actions = get_game_actions()
    game_actions_recursive(game_state, actions)


def game_actions_recursive(game_state: GameState, actions: dict) -> None:
    """
    Recursively handle game actions.

    Args:
        game_state (GameState): The current state of the game.
        actions (dict): Dictionary mapping choices to their handlers.
    """
    display_game_actions(actions)
    choice = prompt_action(len(actions))

    game_state = handle_action(choice, game_state, actions)
    if game_state is not None:  # Continue recursion only if not returning to main menu
        game_actions_recursive(game_state, actions)


def display_game_actions(actions: dict) -> None:
    """
    Display the game actions with options.

    Args:
        actions (dict): The game actions dictionary.
    """
    print("Choose a Game Action:")
    for key, (description, _) in actions.items():
        print(f"{key}. {description}")


def prompt_action(num_options: int) -> str:
    """
    Prompt the user for a valid action choice.

    Args:
        num_options (int): The number of available options.

    Returns:
        str: The user's valid action choice.
    """
    choice = input("> ")
    if choice.isdigit() and 1 <= int(choice) <= num_options:
        return choice
    else:
        display_invalid_input(f"Invalid choice. Please enter a number between 1 and {num_options}.")
        return prompt_action(num_options)


def handle_action(choice: str, game_state: GameState, actions: dict) -> GameState:
    """
    Handle the user's action choice.

    Args:
        choice (str): The user's action choice.
        game_state (GameState): The current state of the game.
        actions (dict): Dictionary mapping choices to their handlers.

    Returns:
        GameState: The updated state of the game or None if returning to main menu.
    """
    action = actions.get(choice)
    if action:
        _, handler = action
        if handler:
            return handler(game_state)
        else:
            # Handle "Back to main menu"
            return None
    print("Invalid choice. Please enter a valid number.")
    return game_state
