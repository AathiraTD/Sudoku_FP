from dataclasses import dataclass
from typing import Tuple, Dict, Optional, Union
from core_data.cell import Cell
from core_data.coordinate import Coordinate
from core_data.grid.row import Row
from core_data.cell_state import CellState
from core_data.cell_value import CellValue


@dataclass(frozen=True)
class Grid:
    rows: Tuple[Row, ...]
    grid_size: int

    def __new__(cls, rows: Tuple[Row, ...], grid_size: int):
        instance = super(Grid, cls).__new__(cls)
        object.__setattr__(instance, 'rows', rows)
        object.__setattr__(instance, 'grid_size', grid_size)
        return instance

    def __getitem__(self, index: Union[int, Tuple[int, int]]) -> Union[Row, Cell]:
        if isinstance(index, int):
            return self.rows[index]
        elif isinstance(index, tuple) and len(index) == 2:
            try:
                coord = Coordinate(index[0], index[1], self.grid_size)
                return self.rows[index[0]].cells[coord]
            except ValueError:
                raise IndexError("Invalid index")
        raise IndexError("Invalid index")

    @staticmethod
    def create(grid_size: int, cells: Optional[Dict[Coordinate, Cell]] = None) -> "Grid":
        if cells is None:
            cells = {}

            def init_cells(row: int, col: int) -> None:
                if row >= grid_size:
                    return
                if col >= grid_size:
                    init_cells(row + 1, 0)
                else:
                    coord = Coordinate(row, col, grid_size)
                    cells[coord] = Cell(value=CellValue(None, grid_size), state=CellState.EMPTY)
                    init_cells(row, col + 1)

            init_cells(0, 0)
        rows = tuple(
            Row({coord: cells[coord] for coord in cells if coord.row_index == row_index}, row_index) for row_index in
            range(grid_size))
        return Grid(rows=rows, grid_size=grid_size)


