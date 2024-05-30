from dataclasses import dataclass
from types import MappingProxyType
from typing import Dict, Tuple, List, Set

from core_data.cell import Cell
from core_data.cell_state import CellState
from core_data.coordinate import Coordinate


@dataclass(frozen=True)
class Column:
    """Represents a column in a Sudoku grid with immutable cells and column index."""
    cells: MappingProxyType  # An immutable dictionary of Coordinate keys and Cell values
    column_index: int  # The index of the column

    def __new__(cls, cells: Dict[Coordinate, Cell], column_index: int):
        # Convert the cells dictionary to an immutable MappingProxyType
        immutable_cells = MappingProxyType(cells)
        # Validate the cells before creating the instance
        valid, message = cls.is_valid(immutable_cells, column_index)
        if not valid:
            raise ValueError(message)
        # Create a new instance using the superclass
        instance = super(Column, cls).__new__(cls)
        # Set the instance attributes cells and column_index
        object.__setattr__(instance, 'cells', immutable_cells)
        object.__setattr__(instance, 'column_index', column_index)
        # Return the new instance
        return instance

    @staticmethod
    def is_valid(cells: MappingProxyType, column_index: int) -> Tuple[bool, str]:
        def validate_cells(cell_in_cells: List[Tuple[Coordinate, Cell]], index: int, values_tracked: Set[int]) -> Tuple[
            bool, str]:
            if index >= len(cell_in_cells):
                return True, "Column is valid."

            coord, cell = cell_in_cells[index]

            # Check if coordinate is in the specified column
            if coord.col_index != column_index:
                return False, f"Coordinate {coord} is not in the specified column {column_index}."

            # Validate the cell itself
            valid_cell, message = Cell.is_valid(cell.value, cell.state)
            if not valid_cell:
                return False, f"Invalid cell at {coord}: {message}"

            value = cell.value.value

            # Check for unique values in PRE_FILLED and HINT states. Checks are not done for user filled cells
            if cell.state is not CellState.USER_FILLED and value is not None:
                if value in values_tracked:
                    return False, f"Duplicate value {value} found in the column."
                values_tracked.add(value)

            return validate_cells(cell_in_cells, index + 1, values_tracked)

        # Convert dictionary items to a list for recursive processing
        cells_items = list(cells.items())
        values_seen = set()

        # Start the recursive validation
        return validate_cells(cells_items, 0, values_seen)

    def __getitem__(self, row_index: int) -> Cell:
        coord = Coordinate(row_index, self.column_index, len(self.cells))
        if coord not in self.cells:
            raise IndexError("Row index out of range.")
        return self.cells[coord]

    @classmethod
    def create(cls, cells: Dict[Coordinate, Cell], column_index: int) -> 'Column':
        # Create a Column instance
        return cls(cells, column_index)
