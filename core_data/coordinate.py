from typing import Optional, Tuple
from dataclasses import dataclass

@dataclass(frozen=True)
class Coordinate:
    row_index: int  # The row index of the coordinate
    col_index: int  # The column index of the coordinate
    grid_size: int  # The size of the grid

    def __new__(cls, row_index: int, col_index: int, grid_size: int):
        # Validate the row and column values before creating the instance
        if not cls.is_valid(row_index, col_index, grid_size):
            # Raise a ValueError if the coordinates are not valid
            raise ValueError(f"Coordinates must be within the range [0, {grid_size - 1}].")
        # Create a new instance using the superclass (__new__ method of object)
        instance = super(Coordinate, cls).__new__(cls)
        # Set the instance attributes row_index, col_index, and grid_size
        object.__setattr__(instance, 'row_index', row_index)
        object.__setattr__(instance, 'col_index', col_index)
        object.__setattr__(instance, 'grid_size', grid_size)
        # Return the new instance
        return instance

    @staticmethod
    def is_valid(row_index: int, col_index: int, grid_size: int) -> bool:
        # Check if the row and column are within the valid range
        if row_index < 0 or row_index >= grid_size:
            # The row is out of the valid range
            return False
        if col_index < 0 or col_index >= grid_size:
            # The column is out of the valid range
            return False
        # Both row and column are within the valid range
        return True

    @staticmethod
    def create(row_index: int, col_index: int, grid_size: int) -> Tuple[Optional['Coordinate'], Optional[str]]:
        # Try to create a Coordinate instance, handle ValueError if coordinates are invalid
        try:
            # Return a new Coordinate instance and None for the error
            return Coordinate(row_index, col_index, grid_size), None
        except ValueError as e:
            # Return None for the instance and the error message if coordinates are invalid
            return None, str(e)

    def __lt__(self, other: 'Coordinate') -> bool:
        if self.row_index == other.row_index:
            return self.col_index < other.col_index
        return self.row_index < other.row_index
