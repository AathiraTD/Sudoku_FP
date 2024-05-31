import unittest
from dataclasses import FrozenInstanceError

from core_data.cell_value import CellValue


class TestCellValue(unittest.TestCase):

    def test_valid_value_creation(self):
        # Test creating a valid CellValue with an integer within the range
        cell_value, error = CellValue.create(5, 10)
        self.assertIsNotNone(cell_value)
        self.assertIsNone(error)
        self.assertEqual(cell_value.value, 5)
        self.assertEqual(cell_value.max_value, 10)

    def test_valid_none_value_creation(self):
        # Test creating a valid CellValue with None as the value
        cell_value, error = CellValue.create(None, 10)
        self.assertIsNotNone(cell_value)
        self.assertIsNone(error)
        self.assertIsNone(cell_value.value)
        self.assertEqual(cell_value.max_value, 10)

    def test_invalid_value_above_max(self):
        # Test creating a CellValue with a value above the max_value
        cell_value, error = CellValue.create(15, 10)
        self.assertIsNone(cell_value)
        self.assertIsNotNone(error)
        self.assertEqual(error, "CellValue must be between 1 and 10, or None.")

    def test_invalid_value_below_min(self):
        # Test creating a CellValue with a value below the minimum (1)
        cell_value, error = CellValue.create(0, 10)
        self.assertIsNone(cell_value)
        self.assertIsNotNone(error)
        self.assertEqual(error, "CellValue must be between 1 and 10, or None.")

    def test_is_valid_method(self):
        # Test the is_valid static method with various inputs
        self.assertTrue(CellValue.is_valid(None, 10))
        self.assertTrue(CellValue.is_valid(5, 10))
        self.assertFalse(CellValue.is_valid(11, 10))
        self.assertFalse(CellValue.is_valid(0, 10))

    def test_frozen_dataclass(self):
        # Test that the CellValue class is frozen (immutable)
        cell_value = CellValue(5, 10)
        with self.assertRaises(FrozenInstanceError):
            cell_value.value = 7

    def test_edge_case_min_value(self):
        # Test creating a CellValue with the minimum valid value
        cell_value, error = CellValue.create(1, 10)
        self.assertIsNotNone(cell_value)
        self.assertIsNone(error)
        self.assertEqual(cell_value.value, 1)
        self.assertEqual(cell_value.max_value, 10)

    def test_edge_case_max_value(self):
        # Test creating a CellValue with the maximum valid value
        cell_value, error = CellValue.create(10, 10)
        self.assertIsNotNone(cell_value)
        self.assertIsNone(error)
        self.assertEqual(cell_value.value, 10)
        self.assertEqual(cell_value.max_value, 10)

    def test_invalid_max_value_less_than_min(self):
        # Test creating a CellValue where max_value is less than the minimum value range
        cell_value, error = CellValue.create(5, 0)
        self.assertIsNone(cell_value)
        self.assertIsNotNone(error)
        self.assertEqual(error, "CellValue must be between 1 and 0, or None.")


if __name__ == '__main__':
    unittest.main()
