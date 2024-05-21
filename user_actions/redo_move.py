from core_data.cell_state import CellState
from core_data.coordinate import Coordinate
from core_data.game_state import GameState
from core_data.grid.grid import update_cell


def redo_move(game_state: GameState) -> GameState:
    """
    Redo the last undone action.
    """
    try:
        action, game_state = game_state.pop_redo()
        if action is None:
            print("No more actions to redo.")
            return game_state

        row, col, new_value = action

        # Push the current state to the undo stack
        game_state = game_state.push_undo((row, col, game_state.grid[row, col].value.value))

        # Apply the grid to the new value
        new_grid = update_cell(game_state.grid, Coordinate(row, col, game_state.grid.grid_size), new_value, CellState.USER_FILLED)
        return game_state.with_grid(new_grid)
    except ValueError as e:
        print(f"Redo operation failed: {e}")
        return game_state
    except Exception as e:
        print(f"An unexpected error occurred during redo: {e}")
        return game_state