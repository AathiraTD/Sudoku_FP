import unittest
from io import StringIO
from unittest.mock import patch

from colorama import Style, Fore

from core_data.cell import Cell
from core_data.cell_state import CellState
from core_data.cell_value import CellValue
from core_data.coordinate import Coordinate
from core_data.grid import Grid
from user_interface.display.display_grid import display_messages, get_row_label, print_row, display_grid


class TestGridDisplayFunctions(unittest.TestCase):
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

    @patch('sys.stdout', new_callable=StringIO)
    def test_display_grid(self, mock_stdout):
        # Test the grid display function
        display_grid(self.grid)
        output = mock_stdout.getvalue().strip()
        # Check for the presence of some expected strings
        self.assertIn("A |", output)
        self.assertIn("1", output)
        self.assertIn("2", output)
        self.assertIn(".", output)
        self.assertIn(Fore.GREEN + " 1 " + Style.RESET_ALL, output)
        self.assertIn(Fore.GREEN + " 2 " + Style.RESET_ALL, output)
        self.assertIn("   ------------------------------------", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_print_row(self, mock_stdout):
        # Test the row printing function
        print_row(self.grid, 0)
        output = mock_stdout.getvalue().strip()
        self.assertIn("A |", output)
        self.assertIn(Fore.GREEN + " 1 " + Style.RESET_ALL, output)
        self.assertIn(Fore.GREEN + " 2 " + Style.RESET_ALL, output)
        self.assertIn(" . ", output)
        self.assertIn("|", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_display_messages(self, mock_stdout):
        # Test the display messages function
        messages = ["Message 1", "Message 2", "Message 3"]
        display_messages(messages)
        output = mock_stdout.getvalue().strip()
        self.assertIn("Message 1", output)
        self.assertIn("Message 2", output)
        self.assertIn("Message 3", output)

    def test_get_row_label(self):
        # Test the row label conversion function
        self.assertEqual(get_row_label(0), 'A')
        self.assertEqual(get_row_label(1), 'B')
        self.assertEqual(get_row_label(25), 'Z')


if __name__ == "__main__":
    unittest.main()
