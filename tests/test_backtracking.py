import unittest
from unittest.mock import patch

from core_data.cell import Cell
from core_data.cell_state import CellState
from core_data.cell_value import CellValue
from core_data.coordinate import Coordinate
from core_data.grid import Grid
from puzzle_handler.puzzle_solver.puzzle_solver import backtrack


class TestBacktrackingSolver(unittest.TestCase):
    def setUp(self):
        self.grid_size = 9
        self.cells = {
            Coordinate(0, 0, self.grid_size): Cell(CellValue(5, self.grid_size), CellState.PRE_FILLED),
            Coordinate(0, 1, self.grid_size): Cell(CellValue(3, self.grid_size), CellState.PRE_FILLED),
            Coordinate(0, 4, self.grid_size): Cell(CellValue(7, self.grid_size), CellState.PRE_FILLED),
            Coordinate(1, 0, self.grid_size): Cell(CellValue(6, self.grid_size), CellState.PRE_FILLED),
            Coordinate(1, 3, self.grid_size): Cell(CellValue(1, self.grid_size), CellState.PRE_FILLED),
            Coordinate(1, 4, self.grid_size): Cell(CellValue(9, self.grid_size), CellState.PRE_FILLED),
            Coordinate(1, 5, self.grid_size): Cell(CellValue(5, self.grid_size), CellState.PRE_FILLED),
            Coordinate(2, 1, self.grid_size): Cell(CellValue(9, self.grid_size), CellState.PRE_FILLED),
            Coordinate(2, 2, self.grid_size): Cell(CellValue(8, self.grid_size), CellState.PRE_FILLED),
            Coordinate(2, 7, self.grid_size): Cell(CellValue(6, self.grid_size), CellState.PRE_FILLED),
            # Rest of the cells will be empty for simplicity
        }
        self.grid = Grid.create(grid_size=self.grid_size, cells=self.cells)

    @patch('puzzle_handler.puzzle_solver.puzzle_solver.apply_naked_singles')
    @patch('puzzle_handler.puzzle_solver.puzzle_solver.find_empty_cell_with_fewest_options')
    @patch('puzzle_handler.puzzle_solver.puzzle_solver.sort_values_by_constraints')
    def test_backtrack_solved(self, mock_sort_values_by_constraints, mock_find_empty_cell, mock_apply_naked_singles):
        # Mock dependencies
        mock_apply_naked_singles.return_value = self.grid
        mock_find_empty_cell.return_value = None  # No empty cells, puzzle is solved
        mock_sort_values_by_constraints.side_effect = lambda grid, row, col, values: values

        solved_grid, success = backtrack(self.grid)

        self.assertTrue(success)
        self.assertEqual(solved_grid, self.grid)

    @patch('puzzle_handler.puzzle_solver.puzzle_solver.apply_naked_singles')
    @patch('puzzle_handler.puzzle_solver.puzzle_solver.find_empty_cell_with_fewest_options')
    @patch('puzzle_handler.puzzle_solver.puzzle_solver.sort_values_by_constraints')
    @patch('puzzle_handler.puzzle_solver.puzzle_solver.is_valid')
    def test_backtrack_unsolved(self, mock_is_valid, mock_sort_values_by_constraints, mock_find_empty_cell,
                                mock_apply_naked_singles):
        # Mock dependencies
        mock_apply_naked_singles.return_value = self.grid
        mock_find_empty_cell.return_value = (0, 2)  # Mock an empty cell at (0, 2)
        mock_sort_values_by_constraints.side_effect = lambda grid, row, col, values: values
        mock_is_valid.side_effect = lambda grid, row, col, num: num == 4  # Only 4 is valid for this test

        solved_grid, success = backtrack(self.grid)

        self.assertTrue(success)
        self.assertIsNotNone(solved_grid)
        self.assertEqual(solved_grid[0, 2].value.value, 4)

    @patch('puzzle_handler.puzzle_solver.puzzle_solver.apply_naked_singles')
    @patch('puzzle_handler.puzzle_solver.puzzle_solver.find_empty_cell_with_fewest_options')
    @patch('puzzle_handler.puzzle_solver.puzzle_solver.sort_values_by_constraints')
    @patch('puzzle_handler.puzzle_solver.puzzle_solver.is_valid')
    def test_backtrack_no_solution(self, mock_is_valid, mock_sort_values_by_constraints, mock_find_empty_cell,
                                   mock_apply_naked_singles):
        # Mock dependencies
        mock_apply_naked_singles.return_value = self.grid
        mock_find_empty_cell.return_value = (0, 2)  # Mock an empty cell at (0, 2)
        mock_sort_values_by_constraints.side_effect = lambda grid, row, col, values: values
        mock_is_valid.return_value = False  # No valid numbers for this test

        solved_grid, success = backtrack(self.grid)

        self.assertFalse(success)
        self.assertEqual(solved_grid, self.grid)


if __name__ == "__main__":
    unittest.main()
