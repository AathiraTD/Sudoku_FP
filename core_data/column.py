from dataclasses import dataclass
from typing import Dict, Optional, Tuple, Callable
from types import MappingProxyType
from .cell import Cell
from .coordinate import Coordinate

@dataclass(frozen=True)
class Column:
    """Represents a column in a Sudoku grid with immutable cells and column index."""
    cells: MappingProxyType  # An immutable dictionary of Coordinate keys and Cell values
    column_index: int  # The index of the column

    def __new__(cls, cells: Dict[Coordinate, Cell], column_index: int):
        """
        Create a new Column instance with immutable cells.
        """
        # Convert the cells dictionary to an immutable MappingProxyType
        immutable_cells = MappingProxyType(cells)

        # Validate the cells before creating the instance
        if not cls.is_valid(immutable_cells, column_index):
            raise ValueError(
                "All elements of the column must be instances of Cell and values must be unique except for None.")

        # Create a new instance using the superclass (__new__ method of object)
        instance = super(Column, cls).__new__(cls)

        # Set the instance attributes cells and column_index
        object.__setattr__(instance, 'cells', immutable_cells)
        object.__setattr__(instance, 'column_index', column_index)

        # Return the new instance
        return instance

    @staticmethod
    def is_valid(cells: MappingProxyType, column_index: int) -> bool:
        """
        Validate that all cells are in the same column and have unique values.
        """
        # Higher-order function to check if all coordinates are in the specified column
        def all_in_column(coord_checker: Callable[[Coordinate], bool]) -> bool:
            return all(map(coord_checker, cells.keys()))

        # Higher-order function to validate uniqueness of values
        def values_unique(extractor: Callable[[MappingProxyType], list]) -> bool:
            values = extractor(cells)
            return len(values) == len(set(values))

        # Check if all coordinates are in the specified column
        column_check = all_in_column(lambda coord: coord.column == column_index)

        # Check for uniqueness of the values
        uniqueness_check = values_unique(Column._extract_values)

        # Return the combined result of all checks
        return column_check and uniqueness_check

    @staticmethod
    def _extract_values(cells: MappingProxyType, idx: int = 0, values: Optional[list] = None) -> list:
        """
        Extract non-None values from the cells using recursion.
        """
        # Initialize the values list on the first call
        if values is None:
            values = []

        # Base case: if all cells have been processed, return the values list
        if idx == len(cells):
            return values

        # Convert the MappingProxyType to a list to access elements by index
        cell_list = list(cells.values())

        # If the current cell's value is not None, add it to the values list
        if cell_list[idx].value.value is not None:
            values.append(cell_list[idx].value.value)

        # Recursive call to process the next cell
        return Column._extract_values(cells, idx + 1, values)

    @staticmethod
    def _are_values_unique(values: list) -> bool:
        """
        Check if all values are unique.
        """
        # Compare length of values with length of unique values (using set)
        return len(values) == len(set(values))

    def get_cell(self, coordinate: Coordinate) -> Cell:
        """
        Access a specific cell in the column using its coordinate.
        """
        # Check if the coordinate is within the cells and the correct column
        if coordinate.column != self.column_index or coordinate not in self.cells:
            raise IndexError("Coordinate out of range.")

        # Return the cell at the specified coordinate
        return self.cells[coordinate]

    @staticmethod
    def create(cells: Dict[Coordinate, Cell], column_index: int) -> Tuple[Optional['Column'], Optional[str]]:
        """
        Try to create a Column instance, handling ValueError if the cells are invalid.
        """
        try:
            # Attempt to create a new Column instance
            return Column(cells, column_index), None
        except ValueError as e:
            # Return None and the error message if creation fails
            return None, str(e)
