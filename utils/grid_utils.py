import random
from typing import Optional, Tuple, Set, List, Callable, Any, Dict
from core_data.cell_state import CellState
from core_data.cell_value import CellValue
from core_data.grid.grid import Grid, update_grid
from core_data.coordinate import Coordinate
from core_data.cell import Cell


def find_empty_cell(grid: Grid) -> Optional[Tuple[int, int]]:
    def find_cell(row: int, col: int) -> Optional[Tuple[int, int]]:
        if row >= grid.grid_size:
            return None  # Base case: No more rows
        if col >= grid.grid_size:
            return find_cell(row + 1, 0)  # Move to the next row if col exceeds size
        cell = grid[row, col]
        if cell.value.value is None or cell.value.value == 0:
            return row, col  # Empty cell found
        return find_cell(row, col + 1)  # Recursively check the next cell
    return find_cell(0, 0)



def find_random_empty_cell(grid: Grid) -> Optional[Tuple[int, int]]:
    """
    Find a random empty cell in the grid.
    """
    empty_cells = []

    def collect_empty_cells(row_index: int) -> None:
        if row_index >= grid.grid_size:
            return  # Base case: all rows processed
        row = grid.rows[row_index]

        def check_cell(col_index: int) -> None:
            if col_index >= grid.grid_size:
                return  # Base case: all columns processed
            cell = row.cells.get(Coordinate(row_index, col_index, grid.grid_size))
            if cell and (cell.value.value is None or cell.value.value == 0):
                empty_cells.append((row_index, col_index))  # Add empty cell to list
            check_cell(col_index + 1)

        check_cell(0)  # Start checking cells in the current row
        collect_empty_cells(row_index + 1)  # Recursively process the next row

    collect_empty_cells(0)  # Start collecting empty cells from the first row
    return random.choice(empty_cells) if empty_cells else None  # Randomly select an empty cell if available


def remove_cells(grid_size: int, num_cells_to_remove: int) -> Set[Tuple[int, int]]:
    """
    Recursively select cells to remove while ensuring balance across rows, columns, and subgrids.
    """
    subgrid_size = int(grid_size ** 0.5)

    def select_cells(selected_cells: Set[Tuple[int, int]], remaining: int) -> Set[Tuple[int, int]]:
        if remaining == 0:
            return selected_cells  # Base case: no more cells to remove
        row, col = random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)
        subgrid_row, subgrid_col = row // subgrid_size, col // subgrid_size

        if (row, col) in selected_cells:
            return select_cells(selected_cells, remaining)  # Recurse if the cell is already selected

        # Check if selecting this cell would unbalance any row, column, or subgrid
        row_cells = {c for r, c in selected_cells if r == row}
        col_cells = {r for r, c in selected_cells if c == col}
        subgrid_cells = {(r, c) for r, c in selected_cells if
                         r // subgrid_size == subgrid_row and c // subgrid_size == subgrid_col}

        if len(row_cells) >= grid_size - 1 or len(col_cells) >= grid_size - 1 or len(
                subgrid_cells) >= subgrid_size * subgrid_size - 1:
            return select_cells(selected_cells, remaining)  # Recurse if the selection would unbalance

        # Select the cell for removal and recurse
        return select_cells(selected_cells | {(row, col)}, remaining - 1)

    return select_cells(set(), num_cells_to_remove)


def try_values_recursive(values: List[int], callback: Callable[[int, Any], Optional[Any]], context: Any) -> Optional[
    Any]:
    """
    A generic recursive function to try values and apply a callback function.
    """
    if not values:
        return None  # Base case: No values left to try
    result = callback(values[0], context)  # Apply the callback function to the current value
    if result:
        return result  # Return the result if the callback is successful
    return try_values_recursive(values[1:], callback, context)  # Recursive call to try the next value


def label_to_index(label: str, grid_size: int) -> Optional[Tuple[int, int]]:
    """
    Convert a cell label (e.g., 'A1') to a grid index (row, col).
    """
    if len(label) < 2 or not label[0].isalpha() or not label[1:].isdigit():
        return None  # Return None if the format is invalid

    row = ord(label[0].upper()) - ord('A')  # Convert letter to row index
    col = int(label[1:]) - 1  # Convert number to column index

    if row < 0 or col < 0 or row >= grid_size or col >= grid_size:
        return None  # Return None if the index is out of bounds

    return row, col  # Return the valid row and column index


def convert_user_moves(user_input: str, grid_size: int) -> List[Tuple[Coordinate, int]]:
    """
    Convert user input moves to a list of coordinates and values.
    """

    def parse_moves(moves: List[str], index: int, parsed: List[Tuple[Coordinate, int]]) -> List[Tuple[Coordinate, int]]:
        if index >= len(moves):
            return parsed  # Base case: all moves parsed
        move = moves[index]
        if len(move) >= 3:
            row = ord(move[0].upper()) - ord('A')
            col = int(move[1]) - 1
            value = int(move[2])
            if 0 <= row < grid_size and 0 <= col < grid_size:
                parsed.append((Coordinate(row, col, grid_size), value))
        return parse_moves(moves, index + 1, parsed)

    return parse_moves(user_input.replace(" ", "").split(','), 0, [])


def create_empty_grid(grid_size: int = 9) -> Grid:
    """
    Create an empty Sudoku grid.
    """

    def init_cells(row: int, col: int, cells: Dict[Coordinate, Cell]) -> None:
        if row >= grid_size:
            return  # Base case: all rows processed
        if col >= grid_size:
            return init_cells(row + 1, 0, cells)  # Move to the next row if column exceeds grid size
        coord = Coordinate(row, col, grid_size)  # Create a Coordinate for the current cell
        cells[coord] = Cell(value=CellValue(None, grid_size), state=CellState.EMPTY)  # Create an empty Cell
        init_cells(row, col + 1, cells)  # Move to the next column

    cells = {}
    init_cells(0, 0, cells)  # Initialize cells starting from (0, 0)
    return Grid.create(grid_size, cells)  # Return a new Grid instance
