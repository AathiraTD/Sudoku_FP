import os
import json
from typing import Tuple, Dict, Any, List
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
        return file_name, os.getcwd()  # Return the current directory
    elif location_choice == "2":
        directory = input("Enter the custom directory path: ").strip()
        if os.path.isdir(directory):
            return file_name, directory  # Return the custom directory if it exists
        else:
            print("Invalid directory. Saving to the default location instead.")
            return file_name, os.getcwd()  # Use the default directory if the custom one is invalid
    else:
        print("Invalid choice. Saving to the default location instead.")
        return file_name, os.getcwd()  # Use the default directory if the choice is invalid


def convert_cells_to_dict(cells: Dict[Any, Any], keys: List[Any], index: int, result: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """
    Recursively convert cells to a dictionary for serialization.

    Args:
        cells (Dict[Any, Any]): The cells dictionary.
        keys (List[Any]): The list of keys in the cells dictionary.
        index (int): The current index in the list of keys.
        result (Dict[str, Dict[str, Any]]): The result dictionary being built.

    Returns:
        Dict[str, Dict[str, Any]]: The dictionary representation of the cells.
    """
    if index >= len(keys):
        return result  # Base case: all keys have been processed

    key = keys[index]
    coord, cell = key, cells[key]
    result[f"({coord.row_index},{coord.col_index})"] = {
        'value': cell.value.value,
        'state': cell.state.name
    }
    return convert_cells_to_dict(cells, keys, index + 1, result)  # Recursively process the next key


def grid_to_dict(grid: Grid) -> Dict:
    """
    Convert the Grid object to a dictionary for serialization.

    Args:
        grid (Grid): The Grid object.

    Returns:
        Dict: The dictionary representation of the Grid.
    """
    keys = list(grid.cells.keys())
    cells_dict = convert_cells_to_dict(grid.cells, keys, 0, {})
    return {
        'grid_size': grid.grid_size,
        'cells': cells_dict
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
