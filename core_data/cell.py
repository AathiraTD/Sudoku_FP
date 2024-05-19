from dataclasses import dataclass
from typing import Tuple, Optional
from .cell_value import CellValue
from .cell_state import CellState


@dataclass(frozen=True)
class Cell:
    value: CellValue  # The value of the cell, represented by a CellValue instance
    state: CellState  # The state of the cell, represented by a CellState instance

    def __new__(cls, value: CellValue, state: CellState):
        # Validate the value and state before creating the instance
        if not cls.is_valid(value, state):
            # Raise a ValueError if the value or state is not valid
            raise ValueError(f"Invalid Cell: value={value}, state={state}")
        # Create a new instance using the superclass (__new__ method of object)
        instance = super(Cell, cls).__new__(cls)
        # Set the instance attributes value and state
        object.__setattr__(instance, 'value', value)
        object.__setattr__(instance, 'state', state)
        # Return the new instance
        return instance

    @staticmethod
    def is_valid(value: CellValue, state: CellState) -> bool:
        # Check if the value and state are valid
        # Here, we just return True because the value and state are already
        # validated by their respective classes. Customize if more checks are needed.
        return True

    @staticmethod
    def create(value: CellValue, state: CellState) -> Tuple[Optional['Cell'], Optional[str]]:
        # Try to create a Cell instance, handle ValueError if invalid
        try:
            # Return a new Cell instance and None for the error
            return Cell(value, state), None
        except ValueError as e:
            # Return None for the instance and the error message if invalid
            return None, str(e)
