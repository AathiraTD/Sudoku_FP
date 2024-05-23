from dataclasses import dataclass
from types import MappingProxyType
from typing import Dict, Optional, Callable
from core_data.cell import Cell
from core_data.coordinate import Coordinate

@dataclass(frozen=True)
class Row:
    cells: MappingProxyType  # Immutable dictionary of Coordinate keys and Cell values
    row_index: int  # The index of the row

    def __new__(cls, cells: Dict[Coordinate, Cell], row_index: int,):
        # Validate the cells if validation is not skipped
        if not cls.is_valid(cells, row_index):
            raise ValueError("All elements of the row must be instances of Cell and values must be unique except for "
                             "None.")
        immutable_cells = MappingProxyType(cells)
        instance = super(Row, cls).__new__(cls)
        object.__setattr__(instance, 'cells', immutable_cells)
        object.__setattr__(instance, 'row_index', row_index)
        return instance

    @staticmethod
    def is_valid(cells: MappingProxyType, row_index: int) -> bool:
        # Recursive function to check if all coordinates are in the specified row
        def all_in_row(coords: list, index: int) -> bool:
            if index >= len(coords):
                return True
            coord = coords[index]
            if coord.row_index != row_index:
                return False
            return all_in_row(coords, index + 1)

        cell_values = [cell.value.value for cell in cells.values()]
        return all_in_row(list(cells.keys()), 0)

    def get_cell(self, coordinate: Coordinate) -> Cell:
        # Access a specific cell in the row using its coordinate
        if coordinate.row_index != self.row_index or coordinate not in self.cells:
            raise IndexError("Coordinate out of range.")
        return self.cells[coordinate]

    def __getitem__(self, col_index: int) -> Cell:
        # Access a specific cell in the row using its column index
        coord = Coordinate(self.row_index, col_index, len(self.cells))
        if coord not in self.cells:
            raise IndexError("Column index out of range.")
        return self.cells[coord]

    @classmethod
    def create(cls, cells: Dict[Coordinate, Cell], row_index: int) -> 'Row':
        # Create a Row instance
        return cls(cells, row_index)
