import logging

from core_data.grid.grid import Grid
from puzzle_handler.solve.puzzle_solver import update_grid
from core_data.coordinate import Coordinate
from puzzle_handler.techniques.get_possible_values import get_possible_values
from core_data.cell_state import CellState


def apply_naked_singles(grid: Grid) -> Grid:

    grid_size = grid.grid_size  # Get the size of the grid

    def apply_to_cell(row: int, col: int, grid: Grid) -> Grid:

        if row >= grid_size:
            return grid  # Base case: No more rows to process

        if col >= grid_size:
            return apply_to_cell(row + 1, 0, grid)  # Move to the next row if column index exceeds grid size

        try:
            cell = grid[row, col]  # Get the cell at the current row and column
            if cell and cell.value.value is None:
                possible_values = get_possible_values(grid, row, col)  # Get possible values for the cell
                if len(possible_values) == 1:
                    new_value = possible_values.pop()  # If only one possible value, set it
                    coord = Coordinate(row, col, grid_size)  # Create a coordinate for the cell
                    # Update the cell in the grid with a new grid instance
                    grid = update_grid(grid, coord, new_value, CellState.USER_FILLED)

        except Exception as e:
            logging.error(f"Error processing cell at ({row}, {col}): {e}")

        return apply_to_cell(row, col + 1, grid)  # Recursively process the next cell

    return apply_to_cell(0, 0, grid)  # Start the recursion from the first cell





