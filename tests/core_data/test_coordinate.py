import unittest
from dataclasses import FrozenInstanceError

from core_data.coordinate import Coordinate


class TestCoordinate(unittest.TestCase):

    def test_valid_coordinate_creation(self):
        # Test creating a valid coordinate
        coord, error = Coordinate.create(2, 3, 5)
        self.assertIsNotNone(coord)
        self.assertIsNone(error)
        self.assertEqual(coord.row_index, 2)
        self.assertEqual(coord.col_index, 3)
        self.assertEqual(coord.grid_size, 5)

    def test_invalid_row_index(self):
        # Test creating a coordinate with invalid row index
        coord, error = Coordinate.create(-1, 2, 5)
        self.assertIsNone(coord)
        self.assertIsNotNone(error)
        self.assertEqual(error, "Coordinates must be within the range [0, 4].")

    def test_invalid_col_index(self):
        # Test creating a coordinate with invalid column index
        coord, error = Coordinate.create(2, 6, 5)
        self.assertIsNone(coord)
        self.assertIsNotNone(error)
        self.assertEqual(error, "Coordinates must be within the range [0, 4].")

    def test_invalid_row_and_col_index(self):
        # Test creating a coordinate with both invalid row and column indices
        coord, error = Coordinate.create(5, 5, 5)
        self.assertIsNone(coord)
        self.assertIsNotNone(error)
        self.assertEqual(error, "Coordinates must be within the range [0, 4].")

    def test_is_valid_method(self):
        # Test the is_valid static method
        self.assertTrue(Coordinate.is_valid(2, 2, 5))
        self.assertFalse(Coordinate.is_valid(-1, 2, 5))
        self.assertFalse(Coordinate.is_valid(2, 5, 5))
        self.assertFalse(Coordinate.is_valid(5, 5, 5))

    def test_comparison_operator(self):
        # Test the comparison operator
        coord1 = Coordinate(2, 3, 5)
        coord2 = Coordinate(2, 4, 5)
        coord3 = Coordinate(3, 1, 5)

        self.assertTrue(coord1 < coord2)
        self.assertTrue(coord1 < coord3)
        self.assertFalse(coord2 < coord1)
        self.assertFalse(coord3 < coord1)

    def test_frozen_dataclass(self):
        # Test that the Coordinate class is frozen
        coord = Coordinate(2, 3, 5)
        with self.assertRaises(FrozenInstanceError):
            coord.row_index = 1


if __name__ == '__main__':
    unittest.main()
