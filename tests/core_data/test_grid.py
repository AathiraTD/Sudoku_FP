import pytest
from core_data.grid.grid import Grid, update_cell
from core_data.coordinate import Coordinate
from core_data.cell import Cell
from core_data.cell_value import CellValue
from core_data.cell_state import CellState

def create_empty_grid(grid_size):
    cells = {
        Coordinate(row, col, grid_size): Cell(CellValue(None, grid_size), CellState.EMPTY)
        for row in range(grid_size)
        for col in range(grid_size)
    }
    return Grid(cells, grid_size)

def test_grid_creation():
    grid_size = 9
    grid = create_empty_grid(grid_size)
    assert grid.grid_size == grid_size, "Grid size should be 9"
    assert len(grid.cells) == grid_size * grid_size, "Grid should have 81 cells"

def test_grid_getitem():
    grid_size = 9
    grid = create_empty_grid(grid_size)
    coord = Coordinate(0, 0, grid_size)
    cell = grid[0, 0]
    assert cell.value.value is None, "Cell value should be None"
    assert cell.state == CellState.EMPTY, "Cell state should be EMPTY"

def test_grid_update_cell():
    grid_size = 9
    grid = create_empty_grid(grid_size)
    coord = Coordinate(0, 0, grid_size)
    updated_grid = update_cell(grid, coord, 5, CellState.USER_FILLED)
    updated_cell = updated_grid[0, 0]
    assert updated_cell.value.value == 5, "Cell value should be 5"
    assert updated_cell.state == CellState.USER_FILLED, "Cell state should be USER_FILLED"

def test_grid_invalid_update():
    grid_size = 9
    grid = create_empty_grid(grid_size)
    coord = Coordinate(0, 0, grid_size)
    with pytest.raises(ValueError):
        update_cell(grid, coord, 10, CellState.USER_FILLED)

def test_grid_get_row():
    grid_size = 9
    grid = create_empty_grid(grid_size)
    row = grid.get_row(0)
    assert len(row.cells) == grid_size, "Row should have 9 cells"

def test_grid_get_column():
    grid_size = 9
    grid = create_empty_grid(grid_size)
    column = grid.get_column(0)
    assert len(column.cells) == grid_size, "Column should have 9 cells"

def test_grid_get_all_rows():
    grid_size = 9
    grid = create_empty_grid(grid_size)
    rows = grid.get_all_rows(0)
    assert len(rows) == grid_size, "Should return 9 rows"

def test_grid_get_all_columns():
    grid_size = 9
    grid = create_empty_grid(grid_size)
    columns = grid.get_all_columns(0)
    assert len(columns) == grid_size, "Should return 9 columns"

def test_grid_get_all_subgrids():
    grid_size = 9
    grid = create_empty_grid(grid_size)
    subgrids = grid.get_all_subgrids(0, 0, [])
    assert len(subgrids) == (grid_size // 3) ** 2, "Should return 9 subgrids"
