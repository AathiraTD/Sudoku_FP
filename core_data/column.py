from dataclasses import dataclass
from typing import Tuple, Optional, List
from .cell import Cell


@dataclass(frozen=True)
class Column:
    cells: Tuple[Cell, ...]  # A tuple of Cell instances representing the column
    column_index: int  # The index of the column

    def __new__(cls, cells: Tuple[Cell, ...], column_index: int):
        # Validate the cells before creating the instance
        if not cls.is_valid(cells):
            # Raise a ValueError if the cells are not valid
            raise ValueError(
                "All elements of the column must be instances of Cell and values must be unique except for None.")
        # Create a new instance using the superclass (__new__ method of object)
        instance = super(Column, cls).__new__(cls)
        # Set the instance attributes cells and column_index
        object.__setattr__(instance, 'cells', cells)
        object.__setattr__(instance, 'column_index', column_index)
        # Return the new instance
        return instance

    @staticmethod
    def is_valid(cells: Tuple[Cell, ...]) -> bool:
        # Check if all elements are instances of Cell
        if not Column._are_all_cells(cells):
            return False
        # Extract values from cells, ignoring None
        values = Column._extract_values(cells)
        # Check for uniqueness of the values
        return Column._are_values_unique(values)

    @staticmethod
    def _are_all_cells(cells: Tuple[Cell, ...]) -> bool:
        # Recursive check if all elements are instances of Cell
        if not cells:
            return True
        head, *tail = cells
        return isinstance(head, Cell) and Column._are_all_cells(tuple(tail))

    @staticmethod
    def _extract_values(cells: Tuple[Cell, ...], idx: int = 0, values: Optional[List[int]] = None) -> List[int]:
        if values is None:
            values = []
        # Base case: if all cells have been processed
        if idx == len(cells):
            return values
        # Add the cell's value to the list if it is not None
        if cells[idx].value.value is not None:
            values.append(cells[idx].value.value)
        # Recursive call to process the next cell
        return Column._extract_values(cells, idx + 1, values)

    @staticmethod
    def _are_values_unique(values: List[int]) -> bool:
        # Recursive check for uniqueness
        if len(values) <= 1:
            return True
        head, *tail = values
        return head not in tail and Column._are_values_unique(tail)

    @staticmethod
    def create(cells: Tuple[Cell, ...], column_index: int) -> Tuple[Optional['Column'], Optional[str]]:
        # Try to create a Column instance, handle ValueError if the cells are invalid
        try:
            # Return a new Column instance and None for the error
            return Column(cells, column_index), None
        except ValueError as e:
            # Return None for the instance and the error message if the cells are invalid
            return None, str(e)
