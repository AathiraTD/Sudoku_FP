from typing import Optional, Tuple
from dataclasses import dataclass

@dataclass(frozen=True)
class CellValue:
    value: Optional[int]  # The value of the cell, which can be an integer or None
    max_value: int  # The maximum allowed value for the cell

    def __new__(cls, value: Optional[int], max_value: int):
        # Validate the value before creating the instance
        if not cls.is_valid(value, max_value):
            # Raise a ValueError if the value is not valid
            raise ValueError(f"CellValue must be between 1 and {max_value}, or None.")
        # Create a new instance using the superclass (__new__ method of int)
        instance = super(CellValue, cls).__new__(cls, value if value is not None else 0)
        # Set the instance attributes value and max_value
        object.__setattr__(instance, 'value', value)
        object.__setattr__(instance, 'max_value', max_value)
        # Return the new instance
        return instance

    @staticmethod
    def is_valid(value: Optional[int], max_value: int) -> bool:
        # Check if the value is None
        if value is None:
            # If the value is None, it is considered valid
            return True
        else:
            # If the value is not None, check if it is between 1 and max_value
            if 1 <= value <= max_value:
                # The value is within the valid range
                return True
            else:
                # The value is outside the valid range
                return False

    @staticmethod
    def create(value: Optional[int], max_value: int) -> Tuple[Optional['CellValue'], Optional[str]]:
        # Try to create a CellValue instance, handle ValueError if the value is invalid
        try:
            # Return a new CellValue instance and None for the error
            return CellValue(value, max_value), None
        except ValueError as e:
            # Return None for the instance and the error message if the value is invalid
            return None, str(e)
