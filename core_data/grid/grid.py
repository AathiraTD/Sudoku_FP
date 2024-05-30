from dataclasses import dataclass
from typing import Tuple, Dict, Optional, Union

from core_data.cell import Cell
from core_data.cell_state import CellState
from core_data.cell_value import CellValue
from core_data.coordinate import Coordinate
from core_data.grid.row import Row


@dataclass(frozen=True)
class Grid:
    rows: Tuple[Row, ...]
    grid_size: int

    def __new__(cls, rows: Tuple[Row, ...], grid_size: int) -> object:

        # Check the validity of the grid
        if not cls.is_valid(rows, grid_size):
            raise ValueError("Invalid grid configuration")
        instance = super(Grid, cls).__new__(cls)
        object.__setattr__(instance, 'rows', rows)
        object.__setattr__(instance, 'grid_size', grid_size)
        return instance

    def __getitem__(self, index: Union[int, Tuple[int, int], Coordinate]) -> Union[Row, Cell]:
        if isinstance(index, int):
            return self.rows[index]
        elif isinstance(index, Coordinate):
            return self.rows[index.row_index].cells[index]
        elif isinstance(index, tuple) and len(index) == 2:
            coord = Coordinate(index[0], index[1], self.grid_size)
            return self.rows[coord.row_index].cells[coord]
        else:
            raise IndexError("Invalid index")

    @staticmethod
    def create(grid_size: int, cells: Optional[Dict[Coordinate, Cell]] = None) -> object:
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

    def with_updated_cell(self, coord: Coordinate, cell: Cell) -> object:
        new_rows = list(self.rows)
        new_row = new_rows[coord.row_index].with_updated_cell(coord, cell)
        new_rows[coord.row_index] = new_row
        return Grid(tuple(new_rows), self.grid_size)

    def is_valid(rows: Tuple[Row, ...], grid_size: int) -> bool:
        """Check the validity of the grid configuration."""
        return len(rows) == grid_size and all(len(row.cells) == grid_size for row in rows)
