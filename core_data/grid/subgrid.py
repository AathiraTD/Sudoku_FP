from dataclasses import dataclass
from typing import Tuple, Optional, Dict, List
from core_data.cell import Cell
from core_data.cell_state import CellState
from core_data.cell_value import CellValue
from core_data.coordinate import Coordinate


@dataclass(frozen=True)
class Subgrid:
    """Represents a Sudoku subgrid with immutable cells and subgrid size."""
    cells: Tuple[Cell, ...]  # Immutable tuple of Cell objects
    subgrid_size: int  # The size of the subgrid (e.g., 3 for a 9x9 grid)

    def __new__(cls, cells: Tuple[Cell, ...], subgrid_size: int):
        # Validate the cells before creating the instance
        if not cls.is_valid(cells, subgrid_size):
            raise ValueError(f"Subgrid must be {subgrid_size}x{subgrid_size} with unique values in each cell.")
        # Create a new instance using the superclass
        instance = super(Subgrid, cls).__new__(cls)
        # Set the cells attribute
        object.__setattr__(instance, 'cells', cells)
        # Set the subgrid_size attribute
        object.__setattr__(instance, 'subgrid_size', subgrid_size)
        # Return the new instance
        return instance

    @staticmethod
    def is_valid(cells: Tuple[Cell, ...], subgrid_size: int) -> bool:
        def collect_values(index: int, values: List[int]):
            if index == len(cells):
                return values
            cell_value = cells[index].value.value
            if cell_value is not None:
                values.append(cell_value)
            return collect_values(index + 1, values)

        collected_values = collect_values(0, [])
        return len(collected_values) == len(set(collected_values))

    @staticmethod
    def create(subgrid_size: int, cells: Optional[Dict[Coordinate, Cell]] = None) -> "Subgrid":
        # Create a Subgrid instance, optionally with predefined cells
        if cells is None:
            cells = {}  # Initialize an empty dictionary for cells

            def init_cells(row: int, col: int) -> None:
                # Define a recursive function to initialize cells
                if row >= subgrid_size:  # Base case: if row exceeds subgrid size, return
                    return
                if col >= subgrid_size:  # If column exceeds subgrid size, move to next row
                    init_cells(row + 1, 0)
                else:
                    coord = Coordinate(row, col, subgrid_size)  # Create a Coordinate for the current cell
                    cells[coord] = Cell(value=CellValue(None, subgrid_size),
                                        state=CellState.EMPTY)  # Create an empty Cell
                    init_cells(row, col + 1)  # Move to the next column

            init_cells(0, 0)  # Initialize cells starting from (0, 0)

        # Collect the cells in the subgrid
        subgrid_cells = tuple(cells[Coordinate(row, col, subgrid_size)]
                              for row in range(subgrid_size)
                              for col in range(subgrid_size))
        # Return a new Subgrid instance
        return Subgrid(cells=subgrid_cells, subgrid_size=subgrid_size)
