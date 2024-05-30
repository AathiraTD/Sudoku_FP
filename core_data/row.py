from dataclasses import dataclass
from types import MappingProxyType
from typing import Dict, Set, List, Tuple

from core_data.cell import Cell
from core_data.cell_state import CellState
from core_data.coordinate import Coordinate


@dataclass(frozen=True)
class Row:
    cells: MappingProxyType  # Immutable dictionary of Coordinate keys and Cell values
    row_index: int  # The index of the row

    def __new__(cls, cells: Dict[Coordinate, Cell], row_index: int):
        # Validate the cells before creating the Row instance
        valid, message = cls.is_valid(cells, row_index)
        if not valid:
            raise ValueError(message)
        # Create the MappingProxyType after validation
        immutable_cells = MappingProxyType(cells)
        # Create the Row instance
        instance = super(Row, cls).__new__(cls)
        object.__setattr__(instance, 'cells', immutable_cells)
        object.__setattr__(instance, 'row_index', row_index)
        return instance

    @staticmethod
    def is_valid(cells: Dict[Coordinate, Cell], row_index: int) -> Tuple[bool, str]:
        def validate_cells(cell_in_cells: List[Tuple[Coordinate, Cell]], index: int, values_tracked: Set[int]) -> Tuple[
            bool, str]:
            if index >= len(cell_in_cells):
                return True, "Row is valid."

            coord, cell = cell_in_cells[index]

            # Check if coordinate is in the specified row
            if coord.row_index != row_index:
                return False, f"Coordinate {coord} is not in the specified row {row_index}."

            # Validate the cell itself
            valid_cell, message = Cell.is_valid(cell.value, cell.state)
            if not valid_cell:
                return False, f"Invalid cell at {coord}: {message}"

            value = cell.value.value

            # Check for unique values in PRE_FILLED and HINT states. Checks are not done for user filled cells
            if cell.state in {CellState.PRE_FILLED, CellState.HINT} and value is not None:
                if value in values_tracked:
                    return False, f"Duplicate value {value} found in the row."  # Duplicate value found
                values_tracked.add(value)

            return validate_cells(cell_in_cells, index + 1, values_tracked)

        # Convert dictionary items to a list for recursive processing
        cells_items = list(cells.items())
        values_seen = set()

        # Start the recursive validation
        return validate_cells(cells_items, 0, values_seen)

    def __getitem__(self, col_index: int) -> Cell:
        coord = Coordinate(self.row_index, col_index, len(self.cells))
        if coord not in self.cells:
            raise IndexError("Column index out of range.")
        return self.cells[coord]

    @classmethod
    def create(cls, cells: Dict[Coordinate, Cell], row_index: int) -> 'Row':
        return cls(cells, row_index)

    def with_updated_cell(self, coord: Coordinate, cell: Cell) -> 'Row':
        new_cells = dict(self.cells)
        new_cells[coord] = cell
        return Row(cells=new_cells, row_index=self.row_index)
