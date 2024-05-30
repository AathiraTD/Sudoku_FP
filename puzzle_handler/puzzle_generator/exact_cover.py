from typing import List

from core_data.coordinate import Coordinate
from core_data.grid import Grid


def encode_cover(row: int, col: int, num: int, N: int) -> List[int]:
    """Encodes a single constraint in the exact cover matrix for the given row, column, and number."""
    side = N * N
    subgrid_size = int(N ** 0.5)
    cover_row = [0] * (side * 4)
    cover_row[row * N + col] = 1
    cover_row[side + row * N + num - 1] = 1
    cover_row[2 * side + col * N + num - 1] = 1
    cover_row[3 * side + (row // subgrid_size) * subgrid_size * N + (col // subgrid_size) * N + num - 1] = 1
    return cover_row


def sudoku_to_exact_cover(grid: Grid) -> List[List[int]]:
    """Converts the Sudoku grid to an exact cover matrix."""
    N = grid.grid_size
    cover_matrix = []

    def add_row_for_cell(coord: Coordinate, value: int) -> List[int]:
        return encode_cover(coord.row_index, coord.col_index, value, N)

    def process_cells(row: int, col: int) -> List[List[int]]:
        """Recursively process each cell in the grid to add constraints."""
        if row >= N:
            return cover_matrix
        if col >= N:
            return process_cells(row + 1, 0)

        cell = grid[Coordinate(row, col, N)]
        cell_value = cell.value

        if cell_value and cell_value.value is not None:
            cover_matrix.append(add_row_for_cell(Coordinate(row, col, N), cell_value.value))
        else:
            for num in range(1, N + 1):
                cover_matrix.append(add_row_for_cell(Coordinate(row, col, N), num))

        return process_cells(row, col + 1)

    return process_cells(0, 0)
