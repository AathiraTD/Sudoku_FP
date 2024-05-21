import os
import json
from typing import Tuple, Dict
from core_data.grid.grid import Grid
from user_interface.display.display_grid import display_grid


def prompt_for_file_details() -> Tuple[str, str]:
    """
    Prompt the user for the file name and save location.

    Returns:
        Tuple[str, str]: The file name and the directory path.
    """
    # Prompt for file name
    file_name = input("Enter the file name (without extension): ").strip()
    if not file_name.endswith(".json"):
        file_name += ".json"

    # Prompt for save location
    print("Choose the save location:")
    print("1. Default location (current directory)")
    print("2. Custom location")
    location_choice = input("> ").strip()

    if location_choice == "1":
        return file_name, os.getcwd()
    elif location_choice == "2":
        directory = input("Enter the custom directory path: ").strip()
        if os.path.isdir(directory):
            return file_name, directory
        else:
            print("Invalid directory. Saving to the default location instead.")
            return file_name, os.getcwd()
    else:
        print("Invalid choice. Saving to the default location instead.")
        return file_name, os.getcwd()


def grid_to_dict(grid: Grid) -> Dict:
    """
    Convert the Grid object to a dictionary for serialization.

    Args:
        grid (Grid): The Grid object.

    Returns:
        Dict: The dictionary representation of the Grid.
    """
    return {
        'grid_size': grid.grid_size,
        'cells': {
            f"({coord.row_index},{coord.col_index})": {
                'value': cell.value.value,
                'state': cell.state.name
            }
            for coord, cell in grid.cells.items()
        }
    }


def save_game_to_file(grid: Grid) -> None:
    """
    Save the current game state to a file.

    Args:
        grid (Grid): The current state of the Sudoku grid.
    """
    file_name, directory = prompt_for_file_details()
    file_path = os.path.join(directory, file_name)

    # Serialize the game state
    game_state = grid_to_dict(grid)
    with open(file_path, "w") as file:
        json.dump(game_state, file)

    print(f"Game saved successfully to {file_path}")
    display_grid(grid)
