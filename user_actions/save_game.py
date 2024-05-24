import json
import os
from typing import Tuple, Dict

from core_data.coordinate import Coordinate
from core_data.game_state import GameState
from core_data.grid.grid import Grid
from user_interface.user_input_handler import prompt_for_file_details


def game_state_to_dict(game_state: GameState) -> Dict:
    """
    Convert the game state to a dictionary for serialization.

    Args:
        game_state (GameState): The current game state.

    Returns:
        Dict: The game state as a dictionary.
    """
    return {
        "grid": grid_to_dict(game_state.grid),
        "config": game_state.config,
        "hints_used": game_state.hints_used,
        "undo_stack": game_state.undo_stack,
        "redo_stack": game_state.redo_stack
    }


def grid_to_dict(grid: Grid) -> Dict:
    """
    Convert the grid to a dictionary for serialization.

    Args:
        grid (Grid): The Sudoku grid.

    Returns:
        Dict: The grid as a dictionary.
    """

    def convert_cells_to_dict(row_index: int, col_index: int, cells_dict: Dict) -> Dict:
        if row_index >= grid.grid_size:
            return cells_dict

        if col_index >= grid.grid_size:
            return convert_cells_to_dict(row_index + 1, 0, cells_dict)

        coord = Coordinate(row_index, col_index, grid.grid_size)
        cell = grid[coord.row_index, coord.col_index]
        cells_dict[f"({coord.row_index},{coord.col_index})"] = {
            'value': cell.value.value,
            'state': cell.state.name
        }

        return convert_cells_to_dict(row_index, col_index + 1, cells_dict)

    cells_dict = convert_cells_to_dict(0, 0, {})
    return {'grid_size': grid.grid_size, 'cells': cells_dict}


def save_game_to_file(game_state: GameState) -> Tuple[str, str, Dict]:
    """
    Prepare the current game state to be saved to a file.

    Args:
        game_state (GameState): The current game state of the Sudoku game.

    Returns:
        Tuple[str, str, Dict]: The file name, directory, and serialized game state.
    """
    while True:
        file_name, directory = prompt_for_file_details()
        if not file_name:
            print("Invalid input, please enter a valid file name.")
            continue

        if not file_name.endswith(".json"):
            file_name += ".json"

        game_state_dict = game_state_to_dict(game_state)
        return file_name, directory, game_state_dict


def write_to_file(file_name: str, directory: str, data: Dict) -> None:
    """
    Write the data to a file.

    Args:
        file_name (str): The name of the file.
        directory (str): The directory to save the file.
        data (Dict): The data to be saved.
    """
    file_path = os.path.join(directory, file_name)
    try:
        with open(file_path, "w") as file:
            json.dump(data, file)
        print(f"Game saved successfully to {file_path}")
    except IOError as e:
        raise IOError(f"An error occurred while saving the game: {e}")
