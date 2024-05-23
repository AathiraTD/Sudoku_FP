import unittest

from core_data.cell import Cell
from core_data.cell_state import CellState
from core_data.cell_value import CellValue
from core_data.grid.subgrid import Subgrid


class TestSubgrid(unittest.TestCase):
    def setUp(self):
        # Helper to create a cell with a specific value within the allowed range for a 3x3 grid
        self.make_cell = lambda value: Cell(CellValue(value, 3), CellState.PRE_FILLED if value is not None else CellState.EMPTY)

    def test_subgrid_valid_creation(self):
        # All values are within the valid range (1 to 3)
        cells = tuple(self.make_cell(i % 3 + 1) for i in range(9))  # 1, 2, 3, 1, 2, 3, 1, 2, 3
        subgrid = Subgrid(cells, 9)
        self.assertEqual(len(subgrid.cells), 3)

    def test_subgrid_duplicate_values(self):
        # Duplicate values within the allowable range (1 to 3)
        cells = tuple(self.make_cell(1 if i < 3 else i % 3 + 1) for i in range(9))  # 1, 1, 1, 2, 3, 1, 2, 3, 2
        with self.assertRaises(ValueError):
            Subgrid(cells, 3)

    def test_subgrid_invalid_size(self):
        # Providing 8 cells where 9 are expected
        cells = tuple(self.make_cell(i % 3 + 1) for i in range(8))  # Only 8 cells
        with self.assertRaises(ValueError):
            Subgrid(cells, 3)

    def test_subgrid_create_function_without_cells(self):
        # Creation without providing cells should default all to None
        subgrid = Subgrid.create(3)
        for cell in subgrid.cells:
            self.assertIsNone(cell.value.value)
            self.assertEqual(cell.state, CellState.EMPTY)

if __name__ == '__main__':
    unittest.main()
