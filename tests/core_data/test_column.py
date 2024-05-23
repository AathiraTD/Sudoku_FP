import pytest
from core_data.cell import Cell, CellValue, CellState
from core_data.coordinate import Coordinate
from core_data.grid.column import Column

def test_column_creation_valid():
    cells = {
        Coordinate(0, 0, 9): Cell(CellValue(1, 9), CellState.USER_FILLED),
        Coordinate(1, 0, 9): Cell(CellValue(2, 9), CellState.USER_FILLED),
        Coordinate(2, 0, 9): Cell(CellValue(3, 9), CellState.USER_FILLED)
    }
    column = Column(cells, 0)
    assert column.column_index == 0
    assert len(column.cells) == 3

def test_column_creation_invalid():
    cells = {
        Coordinate(0, 0, 9): Cell(CellValue(1, 9), CellState.USER_FILLED),
        Coordinate(1, 1, 9): Cell(CellValue(2, 9), CellState.USER_FILLED)  # Invalid: different column
    }
    with pytest.raises(ValueError):
        Column(cells, 0)

def test_column_get_cell():
    cells = {
        Coordinate(0, 0, 9): Cell(CellValue(1, 9), CellState.USER_FILLED),
        Coordinate(1, 0, 9): Cell(CellValue(2, 9), CellState.USER_FILLED)
    }
    column = Column(cells, 0)
    cell = column.get_cell(Coordinate(1, 0, 9))
    assert cell.value.value == 2

def test_column_get_cell_invalid():
    cells = {
        Coordinate(0, 0, 9): Cell(CellValue(1, 9), CellState.USER_FILLED),
        Coordinate(1, 0, 9): Cell(CellValue(2, 9), CellState.USER_FILLED)
    }
    column = Column(cells, 0)
    with pytest.raises(IndexError):
        column.get_cell(Coordinate(1, 1, 9))
