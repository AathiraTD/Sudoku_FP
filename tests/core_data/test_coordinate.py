import pytest
from core_data.coordinate import Coordinate


def test_coordinate_creation_valid():
    coord = Coordinate(row_index=0, col_index=0, grid_size=9)
    assert coord.row_index == 0, "Row index should be 0"
    assert coord.col_index == 0, "Column index should be 0"
    assert coord.grid_size == 9, "Grid size should be 9"


def test_coordinate_creation_invalid():
    with pytest.raises(ValueError):
        Coordinate(row_index=-1, col_index=0, grid_size=9)

    with pytest.raises(ValueError):
        Coordinate(row_index=0, col_index=9, grid_size=9)


def test_coordinate_create_method():
    coord, error = Coordinate.create(row_index=0, col_index=0, grid_size=9)
    assert coord.row_index == 0, "Row index should be 0"
    assert error is None, "Error should be None"

    coord, error = Coordinate.create(row_index=-1, col_index=0, grid_size=9)
    assert coord is None, "Coordinate should be None"
    assert error is not None, "Error should not be None"


def test_coordinate_comparison():
    coord1 = Coordinate(row_index=0, col_index=0, grid_size=9)
    coord2 = Coordinate(row_index=0, col_index=1, grid_size=9)
    assert coord1 < coord2, "coord1 should be less than coord2"
