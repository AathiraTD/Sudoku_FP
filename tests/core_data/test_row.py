import pytest
from core_data.cell import Cell, CellValue, CellState
from core_data.coordinate import Coordinate
from core_data.grid.row import Row

def test_row_creation_valid():
    # Create a set of valid cells for a row
    cells = {
        Coordinate(0, 0, 9): Cell(CellValue(1, 9), CellState.USER_FILLED),
        Coordinate(0, 1, 9): Cell(CellValue(2, 9), CellState.USER_FILLED),
        Coordinate(0, 2, 9): Cell(CellValue(3, 9), CellState.USER_FILLED)
    }
    # Create a Row instance
    row = Row(cells, 0)
    assert row is not None
    assert row.row_index == 0
    assert len(row.cells) == 3

def test_row_creation_invalid():
    # Create a set of invalid cells for a row (cells in different rows)
    cells = {
        Coordinate(0, 0, 9): Cell(CellValue(1, 9), CellState.USER_FILLED),
        Coordinate(1, 1, 9): Cell(CellValue(2, 9), CellState.USER_FILLED)  # Invalid: different row
    }
    # Assert that creating a Row with invalid cells raises a ValueError
    with pytest.raises(ValueError):
        Row(cells, 0)

def test_row_get_cell():
    # Create a set of valid cells for a row
    cells = {
        Coordinate(0, 0, 9): Cell(CellValue(1, 9), CellState.USER_FILLED),
        Coordinate(0, 1, 9): Cell(CellValue(2, 9), CellState.USER_FILLED)
    }
    row = Row(cells, 0)
    assert row is not None
    cell = row.get_cell(Coordinate(0, 1, 9))
    # Assert that the cell's value is correct
    assert cell.value.value == 2

def test_row_get_cell_invalid():
    # Create a set of valid cells for a row
    cells = {
        Coordinate(0, 0, 9): Cell(CellValue(1, 9), CellState.USER_FILLED),
        Coordinate(0, 1, 9): Cell(CellValue(2, 9), CellState.USER_FILLED)
    }
    row = Row(cells, 0)
    assert row is not None
    # Assert that accessing an invalid cell coordinate raises an IndexError
    with pytest.raises(IndexError):
        row.get_cell(Coordinate(1, 1, 9))

def test_row_getitem():
    # Create a set of valid cells for a row
    cells = {
        Coordinate(0, 0, 9): Cell(CellValue(1, 9), CellState.USER_FILLED),
        Coordinate(0, 1, 9): Cell(CellValue(2, 9), CellState.USER_FILLED),
        Coordinate(0, 2, 9): Cell(CellValue(3, 9), CellState.USER_FILLED),
        Coordinate(0, 3, 9): Cell(CellValue(4, 9), CellState.USER_FILLED),
        Coordinate(0, 4, 9): Cell(CellValue(5, 9), CellState.USER_FILLED),
        Coordinate(0, 5, 9): Cell(CellValue(6, 9), CellState.USER_FILLED),
        Coordinate(0, 6, 9): Cell(CellValue(7, 9), CellState.USER_FILLED),
        Coordinate(0, 7, 9): Cell(CellValue(8, 9), CellState.USER_FILLED),
        Coordinate(0, 8, 9): Cell(CellValue(9, 9), CellState.USER_FILLED),
    }
    row = Row(cells, 0)
    assert row is not None
    # Assert that accessing a cell using its column index returns the correct value
    assert row[1].value.value == 2
