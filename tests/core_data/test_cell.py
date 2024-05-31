import unittest
from dataclasses import FrozenInstanceError
from enum import Enum

from core_data.cell import Cell
from core_data.cell_state import CellState
from core_data.cell_value import CellValue


class TestCell(unittest.TestCase):

    def setUp(self):
        # Setting up valid CellValue and CellState instances for reuse in tests
        self.valid_cell_value = CellValue(5, 9)
        self.valid_none_cell_value = CellValue(None, 9)
        self.cell_state_prefilled = CellState.PRE_FILLED
        self.cell_state_user_filled = CellState.USER_FILLED
        self.cell_state_hint = CellState.HINT
        self.cell_state_empty = CellState.EMPTY

    def test_valid_cell_creation(self):
        # Test creating a valid Cell instance with a valid CellValue and CellState
        cell, error = Cell.create(self.valid_cell_value, self.cell_state_user_filled)
        self.assertIsNotNone(cell)
        self.assertIsNone(error)
        self.assertEqual(cell.value, self.valid_cell_value)
        self.assertEqual(cell.state, self.cell_state_user_filled)

    def test_valid_none_value_cell_creation(self):
        # Test creating a valid Cell instance with a None CellValue and valid CellState
        cell, error = Cell.create(self.valid_none_cell_value, self.cell_state_empty)
        self.assertIsNotNone(cell)
        self.assertIsNone(error)
        self.assertEqual(cell.value, self.valid_none_cell_value)
        self.assertEqual(cell.state, self.cell_state_empty)

    def test_invalid_cell_value(self):
        # Test creating a Cell instance with an invalid CellValue
        invalid_cell_value = None
        try:
            invalid_cell_value = CellValue(10, 9)
        except ValueError as e:
            self.assertEqual(str(e), "CellValue must be between 1 and 9, or None.")
            invalid_cell_value = None

        # Ensure invalid_cell_value remains None after catching the exception
        self.assertIsNone(invalid_cell_value)

    def test_invalid_cell_state(self):
        # Test creating a Cell instance with an invalid CellState
        class InvalidCellState(Enum):
            INVALID = "invalid"

        invalid_state = InvalidCellState.INVALID
        cell, error = Cell.create(self.valid_cell_value, invalid_state)
        self.assertIsNone(cell)
        self.assertIsNotNone(error)
        self.assertEqual(error, f"Invalid Cell: CellState {invalid_state} is not valid.")

    def test_frozen_dataclass(self):
        # Test that the Cell class is frozen (immutable)
        cell = Cell(self.valid_cell_value, self.cell_state_prefilled)
        with self.assertRaises(FrozenInstanceError):
            cell.value = CellValue(3, 9)
        with self.assertRaises(FrozenInstanceError):
            cell.state = CellState.USER_FILLED


if __name__ == '__main__':
    unittest.main()
