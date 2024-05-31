import unittest

import numpy as np

from core_data.cell import Cell
from core_data.cell_state import CellState
from core_data.cell_value import CellValue
from core_data.coordinate import Coordinate
from core_data.grid import Grid
from core_data.row import Row


class TestGrid(unittest.TestCase):
    def setUp(self):
        # Set up some test cells and grid for use in the tests
        self.max_value = 9
        self.cells = {
            Coordinate(0, 0, self.max_value): Cell(CellValue(1, self.max_value), CellState.PRE_FILLED),
            Coordinate(0, 1, self.max_value): Cell(CellValue(2, self.max_value), CellState.PRE_FILLED),
            Coordinate(0, 2, self.max_value): Cell(CellValue(None, self.max_value), CellState.EMPTY),
            Coordinate(1, 0, self.max_value): Cell(CellValue(3, self.max_value), CellState.PRE_FILLED),
            Coordinate(1, 1, self.max_value): Cell(CellValue(4, self.max_value), CellState.PRE_FILLED),
            Coordinate(1, 2, self.max_value): Cell(CellValue(5, self.max_value), CellState.PRE_FILLED),
            Coordinate(2, 0, self.max_value): Cell(CellValue(6, self.max_value), CellState.PRE_FILLED),
            Coordinate(2, 1, self.max_value): Cell(CellValue(7, self.max_value), CellState.PRE_FILLED),
            Coordinate(2, 2, self.max_value): Cell(CellValue(8, self.max_value), CellState.PRE_FILLED),
        }
        self.grid = Grid.create(grid_size=9, cells=self.cells)

    def test_grid_creation(self):
        # Test if the grid is created successfully
        grid = Grid.create(grid_size=9, cells=self.cells)
        self.assertIsInstance(grid, Grid)
        self.assertEqual(grid.grid_size, 9)

    def test_grid_retrieval_by_index(self):
        # Test retrieving a row by its index
        row = self.grid[0]
        self.assertIsInstance(row, Row)
        self.assertEqual(row.row_index, 0)

        # Test retrieving a cell by its coordinate
        cell = self.grid[Coordinate(0, 0, self.max_value)]
        self.assertIsInstance(cell, Cell)
        self.assertEqual(cell.value.value, 1)

        # Test retrieving a cell by row and column indices
        cell = self.grid[0, 1]
        self.assertEqual(cell.value.value, 2)

    def test_grid_update_cell(self):
        # Test updating a cell in the grid
        coord = Coordinate(0, 2, self.max_value)
        new_cell = Cell(CellValue(9, self.max_value), CellState.USER_FILLED)
        updated_grid = self.grid.with_updated_cell(coord, new_cell)
        self.assertNotEqual(self.grid, updated_grid)
        self.assertEqual(updated_grid[coord].value.value, 9)
        self.assertEqual(updated_grid[coord].state, CellState.USER_FILLED)

    def test_grid_validation(self):
        # Test grid validation logic
        valid, message = Grid.is_valid(self.grid.rows, self.grid.grid_size)
        self.assertTrue(valid)
        self.assertEqual(message, "Grid is valid.")

    def test_grid_to_numpy(self):
        # Test conversion of grid to numpy ndarray
        grid_array = self.grid.to_numpy()
        self.assertIsInstance(grid_array, np.ndarray)
        self.assertEqual(grid_array.shape, (9, 9))
        self.assertEqual(grid_array[0, 0], 1)
        self.assertEqual(grid_array[0, 2], 0)

    def test_invalid_grid(self):
        # Test creation of an invalid grid (with invalid cell values)
        invalid_cells = {
            Coordinate(0, 0, self.max_value): Cell(CellValue(1, self.max_value), CellState.PRE_FILLED),
            Coordinate(0, 1, self.max_value): Cell(CellValue(2, self.max_value), CellState.PRE_FILLED),
            Coordinate(0, 2, self.max_value): Cell(CellValue(1, self.max_value), CellState.PRE_FILLED),
            # Duplicate value in the same row
        }
        with self.assertRaises(ValueError):
            Grid.create(grid_size=9, cells=invalid_cells)


if __name__ == "__main__":
    unittest.main()
