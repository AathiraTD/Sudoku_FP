import unittest
from core_data.cell import Cell
from core_data.coordinate import Coordinate
from core_data.cell_state import CellState
from core_data.cell_value import CellValue
from core_data.grid.grid import Grid
from core_data.grid.row import Row
from puzzle_handler.solve.puzzle_solver import update_grid


class TestGrid(unittest.TestCase):

    def setUp(self):
        """
        Set up the initial grid and cell data for testing.
        """
        self.grid_size = 9  # Update grid size to 9 for standard Sudoku
        self.cells = {
            Coordinate(0, 0, self.grid_size): Cell(CellValue(1, self.grid_size), CellState.USER_FILLED),
            Coordinate(0, 1, self.grid_size): Cell(CellValue(2, self.grid_size), CellState.USER_FILLED),
            Coordinate(0, 2, self.grid_size): Cell(CellValue(3, self.grid_size), CellState.USER_FILLED),
            Coordinate(1, 0, self.grid_size): Cell(CellValue(4, self.grid_size), CellState.USER_FILLED),
            Coordinate(1, 1, self.grid_size): Cell(CellValue(5, self.grid_size), CellState.USER_FILLED),
            Coordinate(1, 2, self.grid_size): Cell(CellValue(6, self.grid_size), CellState.USER_FILLED),
            Coordinate(2, 0, self.grid_size): Cell(CellValue(7, self.grid_size), CellState.USER_FILLED),
            Coordinate(2, 1, self.grid_size): Cell(CellValue(8, self.grid_size), CellState.USER_FILLED),
            Coordinate(2, 2, self.grid_size): Cell(CellValue(9, self.grid_size), CellState.USER_FILLED),
        }
        self.grid = Grid.create(grid_size=self.grid_size, cells=self.cells)

    def test_grid_creation(self):
        """
        Test the creation of a Grid object.
        """
        self.assertEqual(self.grid.grid_size, self.grid_size)
        self.assertEqual(len(self.grid.rows), self.grid_size)
        self.assertEqual(self.grid[0, 0].value.value, 1)
        self.assertEqual(self.grid[1, 1].value.value, 5)
        self.assertEqual(self.grid[2, 2].value.value, 9)

    def test_grid_getitem(self):
        """
        Test accessing cells in the grid using __getitem__.
        """
        self.assertIsInstance(self.grid[0], Row)
        self.assertIsInstance(self.grid[0, 0], Cell)
        self.assertEqual(self.grid[0, 0].value.value, 1)
        self.assertEqual(self.grid[1, 1].value.value, 5)
        self.assertEqual(self.grid[2, 2].value.value, 9)

    def test_grid_update_cell(self):
        """
        Test updating a cell in the grid.
        """
        coordinate = Coordinate(0, 0, self.grid_size)
        new_grid = update_grid(self.grid, coordinate, 5, CellState.USER_FILLED)
        self.assertNotEqual(new_grid, self.grid)  # Ensure a new Grid instance is created
        self.assertEqual(new_grid[0, 0].value.value, 5)
        self.assertEqual(new_grid[0, 0].state, CellState.USER_FILLED)

    def test_grid_update_empty_cell(self):
        """
        Test updating an empty cell in the grid.
        """
        new_grid = update_grid(self.grid, Coordinate(0, 0, self.grid_size), None, CellState.EMPTY)
        self.assertEqual(new_grid[0, 0].value.value, None)
        self.assertEqual(new_grid[0, 0].state, CellState.EMPTY)

    def test_grid_create_empty(self):
        """
        Test creating an empty grid.
        """
        empty_grid = Grid.create(grid_size=self.grid_size)
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                self.assertEqual(empty_grid[row, col].value.value, None)
                self.assertEqual(empty_grid[row, col].state, CellState.EMPTY)

    def test_grid_invalid_getitem(self):
        """
        Test invalid access of cells in the grid.
        """
        with self.assertRaises(IndexError):
            _ = self.grid[0, 10]
        with self.assertRaises(IndexError):
            _ = self.grid[10, 0]
        with self.assertRaises(IndexError):
            _ = self.grid[(0, 10)]
        with self.assertRaises(IndexError):
            _ = self.grid[(10, 0)]

if __name__ == "__main__":
    unittest.main()
