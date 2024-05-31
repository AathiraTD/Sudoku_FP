import unittest

from core_data.cell import Cell
from core_data.cell_state import CellState
from core_data.cell_value import CellValue
from core_data.coordinate import Coordinate
from core_data.subgrid import Subgrid


class TestSubgrid(unittest.TestCase):

    def setUp(self):
        # Setting up valid CellValue, CellState, and Coordinate instances for reuse in tests
        self.cell_value_1 = CellValue(1, 9)
        self.cell_value_2 = CellValue(2, 9)
        self.cell_value_none = CellValue(None, 9)

        self.cell_prefilled_1 = Cell(self.cell_value_1, CellState.PRE_FILLED)
        self.cell_prefilled_2 = Cell(self.cell_value_2, CellState.PRE_FILLED)
        self.cell_user_filled = Cell(self.cell_value_none, CellState.USER_FILLED)
        self.cell_hint_1 = Cell(self.cell_value_1, CellState.HINT)
        self.cell_hint_2 = Cell(self.cell_value_2, CellState.HINT)

        self.coord_0_0 = Coordinate(0, 0, 9)
        self.coord_0_1 = Coordinate(0, 1, 9)
        self.coord_1_0 = Coordinate(1, 0, 9)
        self.coord_1_1 = Coordinate(1, 1, 9)

        self.cells = {
            self.coord_0_0: self.cell_prefilled_1,
            self.coord_0_1: self.cell_prefilled_2,
            self.coord_1_0: self.cell_user_filled,
            self.coord_1_1: self.cell_hint_2,
        }

    def test_valid_subgrid_creation(self):
        # Test creating a valid Subgrid instance
        valid_cells = {
            self.coord_0_0: self.cell_prefilled_1,
            self.coord_0_1: self.cell_prefilled_2,
            self.coord_1_0: self.cell_user_filled,
            self.coord_1_1: Cell(self.cell_value_none, CellState.EMPTY),
        }
        subgrid = Subgrid.create(3, valid_cells)
        self.assertIsInstance(subgrid, Subgrid)
        self.assertEqual(subgrid.subgrid_size, 3)
        self.assertEqual(subgrid.cells[self.coord_0_0], self.cell_prefilled_1)
        self.assertEqual(subgrid.cells[self.coord_0_1], self.cell_prefilled_2)
        self.assertEqual(subgrid.cells[self.coord_1_0], self.cell_user_filled)
        self.assertEqual(subgrid.cells[self.coord_1_1], Cell(self.cell_value_none, CellState.EMPTY))

    def test_duplicate_prefilled_value(self):
        # Test creating a Subgrid with duplicate values in PRE_FILLED cells
        duplicate_cells = {
            self.coord_0_0: self.cell_prefilled_1,
            self.coord_0_1: self.cell_prefilled_1,  # Duplicate value
            self.coord_1_0: self.cell_user_filled,
            self.coord_1_1: Cell(CellValue(3, 9), CellState.EMPTY),  # Ensure unique value
        }
        with self.assertRaises(ValueError) as context:
            Subgrid.create(3, duplicate_cells)
        self.assertIn("Duplicate value 1 found in the subgrid.", str(context.exception))

    def test_duplicate_hint_value(self):
        # Test creating a Subgrid with duplicate values in HINT cells
        duplicate_hint_cells = {
            self.coord_0_0: self.cell_prefilled_1,
            self.coord_0_1: self.cell_hint_1,  # Duplicate value as hint
            self.coord_1_0: self.cell_user_filled,
            self.coord_1_1: Cell(CellValue(3, 9), CellState.EMPTY),  # Ensure unique value
        }
        with self.assertRaises(ValueError) as context:
            Subgrid.create(3, duplicate_hint_cells)
        self.assertIn("Duplicate value 1 found in the subgrid.", str(context.exception))

    def test_get_cell(self):
        # Test the get_cell method
        valid_cells = {
            self.coord_0_0: self.cell_prefilled_1,
            self.coord_0_1: self.cell_prefilled_2,
            self.coord_1_0: self.cell_user_filled,
            self.coord_1_1: Cell(self.cell_value_none, CellState.EMPTY),
        }
        subgrid = Subgrid.create(3, valid_cells)
        self.assertEqual(subgrid.get_cell(self.coord_0_0), self.cell_prefilled_1)
        self.assertEqual(subgrid.get_cell(self.coord_0_1), self.cell_prefilled_2)
        self.assertEqual(subgrid.get_cell(self.coord_1_0), self.cell_user_filled)
        self.assertEqual(subgrid.get_cell(self.coord_1_1), Cell(self.cell_value_none, CellState.EMPTY))
        with self.assertRaises(IndexError):
            _ = subgrid.get_cell(Coordinate(2, 2, 9))  # Coordinate out of range

    def test_getitem(self):
        # Test the __getitem__ method
        valid_cells = {
            self.coord_0_0: self.cell_prefilled_1,
            self.coord_0_1: self.cell_prefilled_2,
            self.coord_1_0: self.cell_user_filled,
            self.coord_1_1: Cell(self.cell_value_none, CellState.EMPTY),
        }
        subgrid = Subgrid.create(3, valid_cells)
        self.assertEqual(subgrid[self.coord_0_0], self.cell_prefilled_1)
        self.assertEqual(subgrid[self.coord_0_1], self.cell_prefilled_2)
        self.assertEqual(subgrid[self.coord_1_0], self.cell_user_filled)
        self.assertEqual(subgrid[self.coord_1_1], Cell(self.cell_value_none, CellState.EMPTY))
        with self.assertRaises(IndexError):
            _ = subgrid[Coordinate(2, 2, 9)]  # Coordinate out of range




if __name__ == '__main__':
    unittest.main()
