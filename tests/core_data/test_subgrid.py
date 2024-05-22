import pytest
from core_data.cell import Cell, CellValue, CellState
from core_data.coordinate import Coordinate
from core_data.grid.subgrid import Subgrid

def test_subgrid_creation_valid():
    cells = {
        Coordinate(0, 0, 9): Cell(CellValue(1, 9), CellState.USER_FILLED),
        Coordinate(0, 1, 9): Cell(CellValue(2, 9), CellState.USER_FILLED),
        Coordinate(0, 2, 9): Cell(CellValue(3, 9), CellState.USER_FILLED),
        Coordinate(1, 0, 9): Cell(CellValue(4, 9), CellState.USER_FILLED),
        Coordinate(1, 1, 9): Cell(CellValue(5, 9), CellState.USER_FILLED),
        Coordinate(1, 2, 9): Cell(CellValue(6, 9), CellState.USER_FILLED),
        Coordinate(2, 0, 9): Cell(CellValue(7, 9), CellState.USER_FILLED),
        Coordinate(2, 1, 9): Cell(CellValue(8, 9), CellState.USER_FILLED),
        Coordinate(2, 2, 9): Cell(CellValue(9, 9), CellState.USER_FILLED),
    }
    subgrid = Subgrid(cells, 0)
    assert subgrid is not None
    assert len(subgrid.cells) == 9

def test_subgrid_creation_invalid():
    cells = {
        Coordinate(0, 0, 9): Cell(CellValue(1, 9), CellState.USER_FILLED),
        Coordinate(0, 1, 9): Cell(CellValue(1, 9), CellState.USER_FILLED),  # Duplicate value
    }
    with pytest.raises(ValueError):
        Subgrid(cells, 0)

def test_subgrid_get_cell():
    cells = {
        Coordinate(0, 0, 9): Cell(CellValue(1, 9), CellState.USER_FILLED),
        Coordinate(0, 1, 9): Cell(CellValue(2, 9), CellState.USER_FILLED),
        Coordinate(0, 2, 9): Cell(CellValue(3, 9), CellState.USER_FILLED),
    }
    subgrid = Subgrid(cells, 0)
    cell = subgrid.get_cell(Coordinate(0, 1, 9))
    assert cell.value.value == 2

def test_subgrid_get_cell_invalid():
    cells = {
        Coordinate(0, 0, 9): Cell(CellValue(1, 9), CellState.USER_FILLED),
        Coordinate(0, 1, 9): Cell(CellValue(2, 9), CellState.USER_FILLED),
        Coordinate(0, 2, 9): Cell(CellValue(3, 9), CellState.USER_FILLED),
    }
    subgrid = Subgrid(cells, 0)
    with pytest.raises(IndexError):
        subgrid.get_cell(Coordinate(1, 1, 9))  # Coordinate not in subgrid

def test_subgrid_create_method():
    cells = {
        Coordinate(0, 0, 9): Cell(CellValue(1, 9), CellState.USER_FILLED),
        Coordinate(0, 1, 9): Cell(CellValue(2, 9), CellState.USER_FILLED),
        Coordinate(0, 2, 9): Cell(CellValue(3, 9), CellState.USER_FILLED),
    }
    subgrid, error = Subgrid.create(cells, 0)
    assert subgrid is not None
    assert error is None

    cells_invalid = {
        Coordinate(0, 0, 9): Cell(CellValue(1, 9), CellState.USER_FILLED),
        Coordinate(0, 1, 9): Cell(CellValue(1, 9), CellState.USER_FILLED),  # Duplicate value
    }
    subgrid, error = Subgrid.create(cells_invalid, 0)
    assert subgrid is None
    assert error is not None