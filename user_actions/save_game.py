import json
import os
from typing import Dict, Any, List

from core_data.coordinate import Coordinate
from core_data.game_state import GameState
from core_data.grid.grid import Grid
from user_interface.display.display_grid import display_grid
from user_interface.user_input_handler import prompt_for_file_details


def convert_cells_to_dict(cells: Dict[Coordinate, Any], keys: List[Coordinate], index: int, result: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:

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

    def convert_cells_to_dict(row_index: int, col_index: int, cells_dict: Dict) -> Dict:
        if row_index >= grid.grid_size:
            return cells_dict

        if col_index >= grid.grid_size:
            return convert_cells_to_dict(row_index + 1, 0, cells_dict)

        coord = Coordinate(row_index, col_index, grid.grid_size)
        cell = grid[coord.row_index,coord.col_index]
        cells_dict[f"({coord.row_index},{coord.col_index})"] = {
            'value': cell.value.value,
            'state': cell.state.name
        }

        return convert_cells_to_dict(row_index, col_index + 1, cells_dict)

    cells_dict = convert_cells_to_dict(0, 0, {})
    return {'grid_size': grid.grid_size, 'cells': cells_dict}


def game_state_to_dict(game_state: GameState) -> Dict:

    return {
        'grid': grid_to_dict(game_state.grid),
        'config': game_state.config,
        'hints_used': game_state.hints_used,
        'undo_stack': game_state.undo_stack,
        'redo_stack': game_state.redo_stack
    }


def save_game_to_file(game_state: GameState) -> None:
    """
    Save the current game state to a file.

    Args:
        game_state (GameState): The current game state of the Sudoku game.
    """
    file_name, directory = prompt_for_file_details()
    file_path = os.path.join(directory, file_name)

    # Serialize the game state
    game_state_dict = game_state_to_dict(game_state)
    with open(file_path, "w") as file:
        json.dump(game_state_dict, file)

    print(f"Game saved successfully to {file_path}")
    display_grid(game_state.grid)
