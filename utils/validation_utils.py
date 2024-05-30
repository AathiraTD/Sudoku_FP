import os
from types import MappingProxyType
from typing import List, Callable

from core_data.column import Column
from core_data.coordinate import Coordinate
from core_data.row import Row
from core_data.subgrid import Subgrid


def validate_grid(cells: MappingProxyType, grid_size: int) -> bool:
    """
    Validate the grid structure, ensuring it is an NxN matrix and each subgrid has unique values.
    """
    # Validate the structure of the grid
    if not validate_structure(cells, grid_size):
        return False

    # Validate all rows
    if not validate_units(cells, grid_size, 0, Row, lambda coord: coord.row_index):
        return False

    # Validate all columns
    if not validate_units(cells, grid_size, 0, Column, lambda coord: coord.col_index):
        return False

    # Validate all sub-grids
    if not validate_subgrids(cells, grid_size, 0, 0):
        return False

    # All validations passed
    return True


def validate_structure(cells: MappingProxyType, grid_size: int) -> bool:
    """
    Ensure all coordinates are within the grid bounds.
    """
    # Check all coordinates within bounds using recursion
    return check_coordinates_within_bounds(list(cells.keys()), grid_size, 0)


def check_coordinates_within_bounds(keys: List[Coordinate], grid_size: int, idx: int) -> bool:
    """
    Recursively check if all coordinates are within the grid bounds.
    """
    # Base case: all coordinates have been checked
    if idx == len(keys):
        return True

    # Get the current coordinate
    coord = keys[idx]

    # Check if the coordinate is within bounds
    if not (0 <= coord.row_index < grid_size and 0 <= coord.col_index < grid_size):
        return False

    # Recursive call to check the next coordinate
    return check_coordinates_within_bounds(keys, grid_size, idx + 1)


def validate_units(cells: MappingProxyType, grid_size: int, index: int, unit_class: Callable,
                   key_func: Callable) -> bool:
    """
    Recursively validate each row or column using the given unit class and key function.
    """
    # Base case: all units have been validated
    if index == grid_size:
        return True

    # Extract cells belonging to the current unit
    unit_cells = {coord: cell for coord, cell in cells.items() if key_func(coord) == index}

    # Create a unit object (Row or Column) and validate it
    unit = unit_class(cells=unit_cells, **{f'{unit_class.__name__.lower()}_index': index})
    if not unit_class.is_valid(unit.cells, index):
        return False

    # Recursive call to validate the next unit
    return validate_units(cells, grid_size, index + 1, unit_class, key_func)


def validate_subgrids(cells: MappingProxyType, grid_size: int, row: int, col: int) -> bool:
    """
    Recursively validate each subgrid in the grid.
    """
    subgrid_size = int(grid_size ** 0.5)

    # Base case: all subgrids have been validated
    if row >= grid_size:
        return True

    # Extract cells belonging to the current subgrid
    subgrid_cells = {
        coord: cell for coord, cell in cells.items()
        if row <= coord.row_index < row + subgrid_size and col <= coord.col_index < col + subgrid_size
    }

    # Calculate the subgrid index
    subgrid_index = (row // subgrid_size) * subgrid_size + (col // subgrid_size)

    # Create a Subgrid object and validate it
    subgrid = Subgrid(cells=subgrid_cells, subgrid_index=subgrid_index)
    if not Subgrid.is_valid(subgrid.cells, subgrid_index):
        return False

    # Calculate the next row and column indices for the next subgrid
    next_col = (col + subgrid_size) % grid_size
    next_row = row + subgrid_size if next_col == 0 else row

    # Recursive call to validate the next subgrid
    return validate_subgrids(cells, grid_size, next_row, next_col)


def validate_directory(directory: str) -> str:
    """
    Validate the directory path. If invalid, use the default directory.

    Args:
        directory (str): The directory path.

    Returns:
        str: The validated directory path.
    """
    if not os.path.isdir(directory):
        print("Invalid directory. Saving to the default location instead.")
        return os.getcwd()
    return directory

