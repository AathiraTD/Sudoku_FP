from dataclasses import dataclass
from typing import Optional, Dict, List, Tuple, Set

from core_data.cell import Cell
from core_data.cell_state import CellState
from core_data.cell_value import CellValue
from core_data.coordinate import Coordinate


@dataclass(frozen=True)
class Subgrid:
    cells: Dict[Coordinate, Cell]
    subgrid_size: int

    def __new__(cls, cells: Dict[Coordinate, Cell], subgrid_size: int):
        valid, message = cls.is_valid(cells, subgrid_size)
        if not valid:
            raise ValueError(message)
        instance = super(Subgrid, cls).__new__(cls)
        object.__setattr__(instance, 'cells', cells)
        object.__setattr__(instance, 'subgrid_size', subgrid_size)
        return instance

    @staticmethod
    def is_valid(cells: Dict[Coordinate, Cell], subgrid_size: int) -> Tuple[bool, str]:
        def validate_cells(coords: List[Coordinate], index: int, values_seen: Set[int]) -> Tuple[bool, str]:
            if index >= len(coords):
                return True, "Subgrid is valid."

            coord = coords[index]
            cell = cells[coord]

            subgrid_row_start = (coord.row_index // subgrid_size) * subgrid_size
            subgrid_col_start = (coord.col_index // subgrid_size) * subgrid_size
            if not (subgrid_row_start <= coord.row_index < subgrid_row_start + subgrid_size and
                    subgrid_col_start <= coord.col_index < subgrid_col_start + subgrid_size):
                return False, f"Coordinate {coord} does not belong to the specified subgrid."

            valid_cell, message = Cell.is_valid(cell.value, cell.state)
            if not valid_cell:
                return False, f"Invalid cell at coordinate {coord}: {message}"

            value = cell.value.value
            if cell.state in {CellState.PRE_FILLED, CellState.HINT} and value is not None:
                if value in values_seen:
                    return False, f"Duplicate value {value} found in the subgrid."
                values_seen.add(value)

            return validate_cells(coords, index + 1, values_seen)

        return validate_cells(list(cells.keys()), 0, set())

    def get_cell(self, coordinate: Coordinate) -> Cell:
        if coordinate not in self.cells:
            raise IndexError("Coordinate out of range.")
        return self.cells[coordinate]

    def __getitem__(self, coordinate: Coordinate) -> Cell:
        return self.get_cell(coordinate)

    @classmethod
    def create(cls, subgrid_size: int, cells: Optional[Dict[Coordinate, Cell]] = None) -> 'Subgrid':
        if cells is None:
            cells = {}

            def init_cells(row: int, col: int) -> None:
                if row >= subgrid_size:
                    return
                if col >= subgrid_size:
                    init_cells(row + 1, 0)
                else:
                    coord = Coordinate(row, col, subgrid_size)
                    if coord not in cells:
                        cells[coord] = Cell(value=CellValue(None, subgrid_size), state=CellState.EMPTY)
                    init_cells(row, col + 1)

            init_cells(0, 0)

        return cls(cells, subgrid_size)
