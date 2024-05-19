from dataclasses import dataclass
from typing import Dict, Optional, Tuple, Union, List, Callable
from types import MappingProxyType
from .cell import Cell
from .coordinate import Coordinate
from .row import Row
from .column import Column
from .subgrid import Subgrid

@dataclass(frozen=True)
class Grid:
    """Represents a Sudoku grid with immutable cells and grid size."""
    cells: MappingProxyType  # An immutable dictionary of Coordinate keys and Cell values
    grid_size: int  # The size of the grid (e.g., 9 for a 9x9 grid)

    def __new__(cls, cells: Dict[Coordinate, Cell], grid_size: int):
        """
        Create a new Grid instance with immutable cells.
        """
        # Convert the cells dictionary to an immutable MappingProxyType
        immutable_cells = MappingProxyType(cells)

        # Validate the cells before creating the instance
        if not cls.is_valid(immutable_cells, grid_size):
            raise ValueError(f"Grid must be {grid_size}x{grid_size} with unique values in each row, column, and subgrid.")

        # Create a new instance using the superclass (__new__ method of object)
        instance = super(Grid, cls).__new__(cls)

        # Set the instance attributes cells and grid_size
        object.__setattr__(instance, 'cells', immutable_cells)
        object.__setattr__(instance, 'grid_size', grid_size)

        # Return the new instance
        return instance

    @staticmethod
    def is_valid(cells: MappingProxyType, grid_size: int) -> bool:
        """
        Validate the grid structure, ensuring it is an NxN matrix and each subgrid has unique values.
        """
        # Validate the structure of the grid
        if not Grid._validate_structure(cells, grid_size):
            return False

        # Validate all rows
        if not Grid._validate_units(cells, grid_size, 0, Row, lambda coord: coord.row):
            return False

        # Validate all columns
        if not Grid._validate_units(cells, grid_size, 0, Column, lambda coord: coord.column):
            return False

        # Validate all subgrids
        if not Grid._validate_subgrids(cells, grid_size, 0, 0):
            return False

        # All validations passed
        return True

    @staticmethod
    def _validate_structure(cells: MappingProxyType, grid_size: int) -> bool:
        """
        Ensure all coordinates are within the grid bounds.
        """
        # Check all coordinates within bounds using recursion
        return Grid._check_coordinates_within_bounds(list(cells.keys()), grid_size, 0)

    @staticmethod
    def _check_coordinates_within_bounds(keys: List[Coordinate], grid_size: int, idx: int) -> bool:
        """
        Recursively check if all coordinates are within the grid bounds.
        """
        # Base case: all coordinates have been checked
        if idx == len(keys):
            return True

        # Get the current coordinate
        coord = keys[idx]

        # Check if the coordinate is within bounds
        if not (0 <= coord.row < grid_size and 0 <= coord.column < grid_size):
            return False

        # Recursive call to check the next coordinate
        return Grid._check_coordinates_within_bounds(keys, grid_size, idx + 1)

    @staticmethod
    def _validate_units(cells: MappingProxyType, grid_size: int, index: int, unit_class: Callable, key_func: Callable) -> bool:
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
        return Grid._validate_units(cells, grid_size, index + 1, unit_class, key_func)

    @staticmethod
    def _validate_subgrids(cells: MappingProxyType, grid_size: int, row: int, col: int) -> bool:
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
            if row <= coord.row < row + subgrid_size and col <= coord.column < col + subgrid_size
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
        return Grid._validate_subgrids(cells, grid_size, next_row, next_col)

    def get_unit(self, index: Union[int, Tuple[int, int], str]) -> Union[Row, Column, Subgrid, Cell, List[Row], List[Column], List[Subgrid]]:
        """
        Access different parts of the grid using various indices.
        """
        if isinstance(index, int):
            # Return a Row object for a single integer index
            return self._get_row(index)
        elif isinstance(index, tuple) and len(index) == 2:
            # Return the Cell object for a tuple index
            return self.cells[Coordinate(index[0], index[1], self.grid_size)]
        elif isinstance(index, str):
            if index == 'row':
                # Return a list of all Row objects
                return self._get_all_rows(0)
            elif index == 'column':
                # Return a list of all Column objects
                return self._get_all_columns(0)
            elif index == 'subgrid':
                # Return a list of all Subgrid objects
                return self._get_all_subgrids(0, 0, [])
        else:
            raise IndexError("Invalid index")

    def _get_row(self, row_index: int) -> Row:
        """
        Get a Row object for a given row index.
        """
        row_cells = {coord: cell for coord, cell in self.cells.items() if coord.row == row_index}
        return Row(cells=row_cells, row_index=row_index)

    def _get_column(self, column_index: int) -> Column:
        """
        Get a Column object for a given column index.
        """
        column_cells = {coord: cell for coord, cell in self.cells.items() if coord.column == column_index}
        return Column(cells=column_cells, column_index=column_index)

    def _get_all_rows(self, index: int) -> List[Row]:
        """
        Recursively get a list of all Row objects.
        """
        # Base case: all rows have been added
        if index == self.grid_size:
            return []

        # Recursive call to get the next row and concatenate with the current row
        return [self._get_row(index)] + self._get_all_rows(index + 1)

    def _get_all_columns(self, index: int) -> List[Column]:
        """
        Recursively get a list of all Column objects.
        """
        # Base case: all columns have been added
        if index == self.grid_size:
            return []

        # Recursive call to get the next column and concatenate with the current column
        return [self._get_column(index)] + self._get_all_columns(index + 1)

    def _get_all_subgrids(self, row: int, col: int, subgrids: List[Subgrid]) -> List[Subgrid]:
        """
        Recursively get a list of all Subgrid objects.
        """
        subgrid_size = int(self.grid_size ** 0.5)

        # Base case: all subgrids have been added
        if row >= self.grid_size:
            return subgrids

        # Extract cells belonging to the current subgrid
        subgrid_cells = {
            coord: cell for coord, cell in self.cells.items()
            if row <= coord.row < row + subgrid_size and col <= coord.column < col + subgrid_size
        }

        # Calculate the subgrid index
        subgrid_index = (row // subgrid_size) * subgrid_size + (col // subgrid_size)

        # Create a Subgrid object and add it to the list
        subgrids.append(Subgrid(cells=subgrid_cells, subgrid_index=subgrid_index))

        # Calculate the next row and column indices for the next subgrid
        next_col = (col + subgrid_size) % self.grid_size
        next_row = row + subgrid_size if next_col == 0 else row

        # Recursive call to add the next subgrid
        return self._get_all_subgrids(next_row, next_col, subgrids)

    @staticmethod
    def create(cells: Dict[Coordinate, Cell], grid_size: int) -> Tuple[Optional['Grid'], Optional[str]]:
        """
        Try to create a Grid instance, handling ValueError if the cells are invalid.
        """
        try:
            # Attempt to create a new Grid instance
            return Grid(cells, grid_size), None
        except ValueError as e:
            # Handle validation errors
            return None, str(e)
