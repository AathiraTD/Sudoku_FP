from dataclasses import dataclass
from typing import Dict, Optional, Tuple, Callable
from types import MappingProxyType
from core_data.cell import Cell
from core_data.coordinate import Coordinate

@dataclass(frozen=True)
class Subgrid:
    """Represents a subgrid in a Sudoku grid with immutable cells and subgrid index."""
    cells: MappingProxyType  # An immutable dictionary of Coordinate keys and Cell values
    subgrid_index: int  # The index of the subgrid

    def __new__(cls, cells: Dict[Coordinate, Cell], subgrid_index: int):
        """
        Create a new Subgrid instance with immutable cells.
        """
        # Convert the cells dictionary to an immutable MappingProxyType
        immutable_cells = MappingProxyType(cells)

        # Validate the cells before creating the instance
        if not cls.is_valid(immutable_cells, subgrid_index):
            raise ValueError(
                "All elements of the subgrid must be instances of Cell and values must be unique except for None.")

        # Create a new instance using the superclass (__new__ method of object)
        instance = super(Subgrid, cls).__new__(cls)

        # Set the instance attributes cells and subgrid_index
        object.__setattr__(instance, 'cells', immutable_cells)
        object.__setattr__(instance, 'subgrid_index', subgrid_index)

        # Return the new instance
        return instance

    @staticmethod
    def is_valid(cells: MappingProxyType, subgrid_index: int) -> bool:
        """
        Validate that all cells have unique values.
        """
        # Higher-order function to validate uniqueness of values
        def values_unique(extractor: Callable[[MappingProxyType], list]) -> bool:
            values = extractor(cells)
            return len(values) == len(set(values))

        # Check for uniqueness of the values
        uniqueness_check = values_unique(Subgrid._extract_values)

        # Return the result of the uniqueness check
        return uniqueness_check

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
        return Subgrid._extract_values(cells, idx + 1, values)

    @staticmethod
    def _are_values_unique(values: list) -> bool:
        """
        Check if all values are unique.
        """
        # Compare length of values with length of unique values (using set)
        return len(values) == len(set(values))

    def get_cell(self, coordinate: Coordinate) -> Cell:
        """
        Access a specific cell in the subgrid using its coordinate.
        """
        # Check if the coordinate is within the cells
        if coordinate not in self.cells:
            raise IndexError("Coordinate out of range.")

        # Return the cell at the specified coordinate
        return self.cells[coordinate]

    @staticmethod
    def create(cells: Dict[Coordinate, Cell], subgrid_index: int) -> Tuple[Optional['Subgrid'], Optional[str]]:
        """
        Try to create a Subgrid instance, handling ValueError if the cells are invalid.
        """
        try:
            # Attempt to create a new Subgrid instance
            return Subgrid(cells, subgrid_index), None
        except ValueError as e:
            # Return None and the error message if creation fails
            return None, str(e)
