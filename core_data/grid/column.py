from dataclasses import dataclass
from types import MappingProxyType
from typing import Dict, Optional, Tuple, List
from core_data.cell import Cell
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
        if not cls.is_valid(immutable_cells, column_index, 0, []):
            raise ValueError("All elements of the column must be instances of Cell and values must be unique except "
                             "for None.")
        # Create a new instance using the superclass
        instance = super(Column, cls).__new__(cls)
        # Set the instance attributes cells and column_index
        object.__setattr__(instance, 'cells', immutable_cells)
        object.__setattr__(instance, 'column_index', column_index)
        # Return the new instance
        return instance

    @staticmethod
    def is_valid(cells: MappingProxyType, column_index: int, idx: int, values: List[int]) -> bool:
        # Base case: if all cells have been processed
        if idx == len(cells):
            return len(values) == len(set(values))

        # Convert the MappingProxyType to a list to access elements by index
        cell_list = list(cells.values())

        # If the current cell's value is not None, add it to the values list
        cell_value = cell_list[idx].value.value
        if cell_value is not None:
            values.append(cell_value)

        # Recursive call to process the next cell
        return Column.is_valid(cells, column_index, idx + 1, values)

    def get_cell(self, coordinate: Coordinate) -> Cell:
        # Access a specific cell in the column using its coordinate
        if coordinate.col_index != self.column_index or coordinate not in self.cells:
            raise IndexError("Coordinate out of range.")
        return self.cells[coordinate]

    def __getitem__(self, row_index: int) -> Cell:
        # Access a specific cell in the column using its row index
        coord = Coordinate(row_index, self.column_index, len(self.cells))
        if coord not in self.cells:
            raise IndexError("Row index out of range.")
        return self.cells[coord]

    @classmethod
    def create(cls, cells: Dict[Coordinate, Cell], column_index: int) -> 'Column':
        # Create a Column instance
        return cls(cells, column_index)
