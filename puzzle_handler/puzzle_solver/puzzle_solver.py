import logging
from functools import lru_cache
from random import random
from typing import Tuple, Optional, List, Callable, Any

from core_data.cell import Cell
from core_data.cell_state import CellState
from core_data.cell_value import CellValue
from core_data.coordinate import Coordinate
from core_data.grid import Grid


@lru_cache(None)
def is_valid(grid: Grid, row: int, col: int, num: int) -> bool:
    grid_size = grid.grid_size
    subgrid_size = int(grid_size ** 0.5)

    def in_row(r: int) -> bool:
        return any(grid[r, c].value.value == num for c in range(grid_size))

    def in_col(c: int) -> bool:
        return any(grid[r, c].value.value == num for r in range(grid_size))

    def in_subgrid(start_row: int, start_col: int) -> bool:
        return any(
            grid[r, c].value.value == num
            for r in range(start_row, start_row + subgrid_size)
            for c in range(start_col, start_col + subgrid_size)
        )

    start_row, start_col = (row // subgrid_size) * subgrid_size, (col // subgrid_size) * subgrid_size
    return not in_row(row) and not in_col(col) and not in_subgrid(start_row, start_col)


@lru_cache(None)
def get_possible_values(grid: Grid, row: int, col: int) -> set:
    grid_size = grid.grid_size
    subgrid_size = int(grid_size ** 0.5)
    possible_values = set(range(1, grid.grid_size + 1))

    def remove_used_values(values: set, r: int, c: int) -> set:
        value = grid[r, c].value.value
        if value:
            values.discard(value)
        return values

    def process_column(idx: int, values: set) -> set:
        if idx >= grid_size:
            return values
        return process_column(idx + 1, remove_used_values(values, row, idx))

    def process_row(idx: int, values: set) -> set:
        if idx >= grid_size:
            return values
        return process_row(idx + 1, remove_used_values(values, idx, col))

    possible_values = process_column(0, possible_values)
    possible_values = process_row(0, possible_values)

    def process_subgrid(r: int, c: int, values: set) -> set:
        if r >= start_row + subgrid_size:
            return values
        if c >= start_col + subgrid_size:
            return process_subgrid(r + 1, start_col, values)
        return process_subgrid(r, c + 1, remove_used_values(values, r, c))

    start_row, start_col = (row // subgrid_size) * subgrid_size, (col // subgrid_size) * subgrid_size
    possible_values = process_subgrid(start_row, start_col, possible_values)

    return possible_values


def find_empty_cell_with_fewest_options(grid: Grid) -> Optional[Tuple[int, int]]:
    min_options = float('inf')
    best_cell = None

    def find_best_cell(row: int, col: int, min_options: int, best_cell: Optional[Tuple[int, int]]) -> Optional[
        Tuple[int, int]]:
        if row >= grid.grid_size:
            return best_cell
        if col >= grid.grid_size:
            return find_best_cell(row + 1, 0, min_options, best_cell)

        if grid[row, col].value.value == 0:
            options = len(get_possible_values(grid, row, col))
            if options < min_options:
                min_options = options
                best_cell = (row, col)

        return find_best_cell(row, col + 1, min_options, best_cell)

    return find_best_cell(0, 0, min_options, best_cell)


def backtrack(grid: Grid) -> Tuple[Grid, bool]:
    logging.debug("Starting backtrack")

    grid = apply_naked_singles(grid)

    empty_cell = find_empty_cell_with_fewest_options(grid)
    if not empty_cell:
        logging.debug("No empty cells found, puzzle solved")
        return grid, True

    row, col = empty_cell
    logging.debug(f"Empty cell found at {row}, {col}")

    def try_values_recursive(values: List[int], callback: Callable[[int, Any], Optional[Any]], context: Any) -> \
            Optional[Any]:
        if not values:
            return None

        result = callback(values[0], context)
        if result:
            return result

        return try_values_recursive(values[1:], callback, context)

    random_values = list(range(1, grid.grid_size + 1))
    random.shuffle(random_values)

    def backtrack_callback(value: int, context: Tuple[Grid, int, int]) -> Optional[Tuple[Grid, bool]]:
        grid, row, col = context
        if is_valid(grid, row, col, value):
            new_grid = grid.with_updated_cell(Coordinate(row, col, grid.grid_size),
                                              Cell(CellValue(value, grid.grid_size), CellState.PRE_FILLED))
            solved_grid, success = backtrack(new_grid)
            if success:
                return solved_grid, True
        return None

    result = try_values_recursive(random_values, backtrack_callback, (grid, row, col))
    return result if result else (grid, False)


def apply_naked_singles(grid: Grid) -> Grid:
    grid_size = grid.grid_size

    def apply_to_cell(row: int, col: int, grid: Grid) -> Grid:
        if row >= grid_size:
            return grid

        if col >= grid_size:
            return apply_to_cell(row + 1, 0, grid)

        cell = grid[row, col]
        if cell and cell.value.value == 0:
            possible_values = get_possible_values(grid, row, col)
            if len(possible_values) == 1:
                new_value = possible_values.pop()
                coord = Coordinate(row, col, grid_size)
                grid = grid.with_updated_cell(coord, Cell(CellValue(new_value, grid_size), CellState.USER_FILLED))

        return apply_to_cell(row, col + 1, grid)

    return apply_to_cell(0, 0, grid)
