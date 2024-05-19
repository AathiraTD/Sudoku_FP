from dataclasses import dataclass
from typing import Tuple, Optional, List
from .cell import Cell


@dataclass(frozen=True)
class Row:
    cells: Tuple[Cell, ...]  # A tuple of Cell instances representing the row
    row_index: int  # The index of the row

    def __new__(cls, cells: Tuple[Cell, ...], row_index: int):
        # Validate the cells before creating the instance
        if not cls.is_valid(cells):
            # Raise a ValueError if the cells are not valid
            raise ValueError(
                "All elements of the row must be instances of Cell and values must be unique except for None.")
        # Create a new instance using the superclass (__new__ method of object)
        instance = super(Row, cls).__new__(cls)
        # Set the instance attributes cells and row_index
        object.__setattr__(instance, 'cells', cells)
        object.__setattr__(instance, 'row_index', row_index)
        # Return the new instance
        return instance

    @staticmethod
    def is_valid(cells: Tuple[Cell, ...]) -> bool:
        # Check if all elements are instances of Cell
        all_cells_valid = Row._are_all_cells(cells)
        if not all_cells_valid:
            return False
        # Extract values from cells, ignoring None
        values = Row._extract_values(cells)
        # Check for uniqueness of the values
        values_unique = Row._are_values_unique(values)
        return values_unique

    @staticmethod
    def _are_all_cells(cells: Tuple[Cell, ...]) -> bool:
        # Recursive check if all elements are instances of Cell
        if not cells:
            # Base case: all elements have been checked
            return True
        # Split the tuple into head (first element) and tail (remaining elements)
        head, *tail = cells
        # Check if the head is an instance of Cell and recursively check the tail
        return isinstance(head, Cell) and Row._are_all_cells(tuple(tail))

    @staticmethod
    def _extract_values(cells: Tuple[Cell, ...], idx: int = 0, values: Optional[List[int]] = None) -> List[int]:
        if values is None:
            values = []
        # Base case: if all cells have been processed
        if idx == len(cells):
            return values
        # Add the cell's value to the list if it is not None
        cell_value = cells[idx].value.value
        if cell_value is not None:
            values.append(cell_value)
        # Recursive call to process the next cell
        return Row._extract_values(cells, idx + 1, values)

    @staticmethod
    def _are_values_unique(values: List[int]) -> bool:
        # Recursive check for uniqueness
        if len(values) <= 1:
            # Base case: a single value or no values are always unique
            return True
        # Split the list into head (first element) and tail (remaining elements)
        head, *tail = values
        # Check if the head is unique in the tail and recursively check the tail
        return head not in tail and Row._are_values_unique(tail)

    @staticmethod
    def create(cells: Tuple[Cell, ...], row_index: int) -> Tuple[Optional['Row'], Optional[str]]:
        # Try to create a Row instance, handle ValueError if the cells are invalid
        try:
            # Return a new Row instance and None for the error
            return Row(cells, row_index), None
        except ValueError as e:
            # Return None for the instance and the error message if the cells are invalid
            return None, str(e)
