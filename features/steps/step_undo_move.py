from core_data.cell_state import CellState
from core_data.coordinate import Coordinate
from core_data.game_state import GameState
from puzzle_handler.solve.puzzle_solver import update_grid
from user_interface.display.display_grid import display_grid


def undo_move(game_state: GameState) -> GameState:
    """
    Undo the last user action.
    """
    try:
        action, new_game_state = game_state.pop_undo()
        if action is None:
            print("No more actions to undo.")
            return new_game_state

        row, col, previous_value = action

        # Push the current state to the redo stack
        new_game_state = new_game_state.push_redo((row, col, new_game_state.grid[row, col].value.value))

        # Revert the grid to the previous value
        new_grid = update_grid(
            new_game_state.grid,
            Coordinate(row, col, new_game_state.grid.grid_size),
            previous_value,
            CellState.USER_FILLED if previous_value != 0 else CellState.EMPTY
        )

        # Display a message indicating which cell was undone
        print(
            f"Undo applied: cell {chr(ord('A') + row)}{col + 1} reverted to {previous_value if previous_value != 0 else 'empty'}.")

        # Display the grid
        display_grid(new_grid)
        return new_game_state.with_grid(new_grid)
    except ValueError as e:
        print(f"Undo operation failed: {e}")
        return game_state
    except Exception as e:
        print(f"An unexpected error occurred during undo: {e}")
        return game_state
