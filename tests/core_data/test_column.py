import unittest

from core_data.cell import Cell
from core_data.cell_state import CellState
from core_data.cell_value import CellValue
from core_data.column import Column
from core_data.coordinate import Coordinate


class TestColumn(unittest.TestCase):

    def setUp(self):
        # Setting up valid CellValue, CellState, and Coordinate instances for reuse in tests
        self.cell_value_1 = CellValue(1, 9)
        self.cell_value_2 = CellValue(2, 9)
        self.cell_value_none = CellValue(None, 9)

        self.cell_prefilled_1 = Cell(self.cell_value_1, CellState.PRE_FILLED)
        self.cell_prefilled_2 = Cell(self.cell_value_2, CellState.PRE_FILLED)
        self.cell_user_filled = Cell(self.cell_value_none, CellState.USER_FILLED)
        self.cell_hint = Cell(self.cell_value_1, CellState.HINT)

        self.coord_0_1 = Coordinate(0, 1, 9)
        self.coord_1_1 = Coordinate(1, 1, 9)
        self.coord_2_1 = Coordinate(2, 1, 9)

        self.cells = {
            self.coord_0_1: self.cell_prefilled_1,
            self.coord_1_1: self.cell_prefilled_2,
            self.coord_2_1: self.cell_user_filled,
        }

    def test_valid_column_creation(self):
        # Test creating a valid Column instance
        column = Column.create(self.cells, 1)
        self.assertIsInstance(column, Column)
        self.assertEqual(column.column_index, 1)
        self.assertEqual(column.cells[self.coord_0_1], self.cell_prefilled_1)
        self.assertEqual(column.cells[self.coord_1_1], self.cell_prefilled_2)
        self.assertEqual(column.cells[self.coord_2_1], self.cell_user_filled)

    def test_invalid_coordinate_in_column(self):
        # Test creating a Column with a coordinate not in the specified column
        invalid_coord = Coordinate(0, 2, 9)
        invalid_cells = {
            invalid_coord: self.cell_prefilled_1,
            self.coord_1_1: self.cell_prefilled_2,
            self.coord_2_1: self.cell_user_filled,
        }
        with self.assertRaises(ValueError) as context:
            Column.create(invalid_cells, 1)
        self.assertIn("Coordinate Coordinate(row_index=0, col_index=2, grid_size=9) is not in the specified column 1.",
                      str(context.exception))

    def test_duplicate_prefilled_value(self):
        # Test creating a Column with duplicate values in PRE_FILLED cells
        duplicate_cells = {
            self.coord_0_1: self.cell_prefilled_1,
            self.coord_1_1: self.cell_prefilled_1,  # Duplicate value
            self.coord_2_1: self.cell_user_filled,
        }
        with self.assertRaises(ValueError) as context:
            Column.create(duplicate_cells, 1)
        self.assertIn("Duplicate value 1 found in the column.", str(context.exception))

    def test_duplicate_hint_value(self):
        # Test creating a Column with duplicate values in HINT cells
        duplicate_hint_cells = {
            self.coord_0_1: self.cell_prefilled_1,
            self.coord_1_1: self.cell_hint,  # Duplicate value as hint
            self.coord_2_1: self.cell_user_filled,
        }
        with self.assertRaises(ValueError) as context:
            Column.create(duplicate_hint_cells, 1)
        self.assertIn("Duplicate value 1 found in the column.", str(context.exception))

    def test_getitem(self):
        # Test the __getitem__ method
        column = Column.create(self.cells, 1)
        self.assertEqual(column[0], self.cell_prefilled_1)
        self.assertEqual(column[1], self.cell_prefilled_2)
        self.assertEqual(column[2], self.cell_user_filled)
        with self.assertRaises(IndexError):
            _ = column[3]  # Index out of range


if __name__ == '__main__':
    unittest.main()
