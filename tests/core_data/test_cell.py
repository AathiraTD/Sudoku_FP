import pytest
from core_data.cell import Cell
from core_data.cell_value import CellValue
from core_data.cell_state import CellState


def test_cell_creation():
    cell_value = CellValue(value=5, max_value=9)
    cell = Cell(value=cell_value, state=CellState.USER_FILLED)
    assert cell.value.value == 5, "Cell value should be 5"
    assert cell.state == CellState.USER_FILLED, "Cell state should be USER_FILLED"


def test_cell_invalid_value():
    with pytest.raises(ValueError):
        CellValue(value=10, max_value=9)
