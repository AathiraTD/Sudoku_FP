from dataclasses import dataclass
from typing import Tuple, Dict, Optional, Union

from core_data.cell import Cell
from core_data.cell_state import CellState
from core_data.cell_value import CellValue
from core_data.column import Column
from core_data.coordinate import Coordinate
from core_data.row import Row


@dataclass(frozen=True)
class Grid:
    rows: Tuple[Row, ...]  # Immutable tuple of Row objects
    grid_size: int  # Size of the grid (e.g., 9 for a 9x9 grid)

    def __new__(cls, rows: Tuple[Row, ...], grid_size: int) -> object:
        # Validate the grid before creating the instance
        valid, message = cls.is_valid(rows, grid_size)
        if not valid:
            raise ValueError(message)  # Raise an error if the grid is not valid
        # Create a new instance using the superclass
        instance = super(Grid, cls).__new__(cls)
        # Set the rows attribute
        object.__setattr__(instance, 'rows', rows)
        # Set the grid_size attribute
        object.__setattr__(instance, 'grid_size', grid_size)
        # Return the new instance
        return instance

    def __getitem__(self, index: Union[int, Tuple[int, int], Coordinate]) -> Union[Row, Cell]:
        # Retrieve a row by its index
        if isinstance(index, int):
            return self.rows[index]
        # Retrieve a cell by its coordinate
        elif isinstance(index, Coordinate):
            return self.rows[index.row_index].cells[index]
        # Retrieve a cell by its row and column indices
        elif isinstance(index, tuple) and len(index) == 2:
            coord = Coordinate(index[0], index[1], self.grid_size)
            return self.rows[coord.row_index].cells[coord]
        else:
            raise IndexError("Invalid index")

    @staticmethod
    def create(grid_size: int, cells: Optional[Dict[Coordinate, Cell]] = None) -> 'Grid':
        if cells is None:
            cells = {}

        # Initialize all cells to be empty initially
        def init_all_cells(row: int, col: int, cells: Dict[Coordinate, Cell]) -> None:
            if row >= grid_size:
                return  # Base case: all rows have been initialized
            if col >= grid_size:
                init_all_cells(row + 1, 0, cells)  # Move to the next row
            else:
                coord = Coordinate(row, col, grid_size)
                if coord not in cells:
                    cells[coord] = Cell(value=CellValue(None, grid_size), state=CellState.EMPTY)
                init_all_cells(row, col + 1, cells)  # Move to the next column

        init_all_cells(0, 0, cells)

        # Create rows from the initialized cells
        rows = tuple(
            Row({coord: cells[coord] for coord in cells if coord.row_index == row_index}, row_index) for row_index in
            range(grid_size)
        )

        # Return a new Grid instance
        return Grid(rows=rows, grid_size=grid_size)

    def with_updated_cell(self, coord: Coordinate, cell: Cell) -> 'Grid':
        # Create a new row with the updated cell
        new_row = self.rows[coord.row_index].with_updated_cell(coord, cell)
        # Create new rows with the updated row
        new_rows = list(self.rows)
        new_rows[coord.row_index] = new_row
        # Return a new Grid instance with the updated rows
        return Grid(tuple(new_rows), self.grid_size)

    @staticmethod
    def is_valid(rows: Tuple[Row, ...], grid_size: int) -> Tuple[bool, str]:
        """Check the validity of the grid configuration."""

        def validate_rows(index: int) -> Tuple[bool, str]:
            # Base case: all rows have been validated
            if index >= len(rows):
                return True, "All rows are valid."
            # Validate the current row
            valid, message = Row.is_valid(rows[index].cells, rows[index].row_index)
            if not valid:
                return False, f"Invalid row {rows[index].row_index}: {message}"
            # Recursively validate the next row
            return validate_rows(index + 1)

        def validate_columns(index: int) -> Tuple[bool, str]:
            # Base case: all columns have been validated
            if index >= grid_size:
                return True, "All columns are valid."

            # Collect the cells for the current column
            def collect_column_cells(row_index: int, column_cells: Dict[Coordinate, Cell]) -> Dict[Coordinate, Cell]:
                if row_index >= grid_size:
                    return column_cells  # Base case: all rows have been processed
                coord = Coordinate(row_index, index, grid_size)
                # Handle missing cells by initializing them if not present
                if coord not in rows[row_index].cells:
                    column_cells[coord] = Cell(value=CellValue(None, grid_size), state=CellState.EMPTY)
                else:
                    column_cells[coord] = rows[row_index].cells[coord]
                return collect_column_cells(row_index + 1, column_cells)  # Recursively collect the next cell

            column_cells = collect_column_cells(0, {})
            # Validate the current column
            valid, message = Column.is_valid(column_cells, index)
            if not valid:
                return False, f"Invalid column {index}: {message}"
            # Recursively validate the next column
            return validate_columns(index + 1)

        # Validate all rows
        valid, message = validate_rows(0)
        if not valid:
            return False, message

        # Validate all columns
        valid, message = validate_columns(0)
        if not valid:
            return False, message

        return True, "Grid is valid."


# Example Usage
def test_grid():
    max_value = 9
    cells = {
        Coordinate(0, 0, max_value): Cell(CellValue(1, max_value), CellState.PRE_FILLED),
        Coordinate(0, 1, max_value): Cell(CellValue(2, max_value), CellState.PRE_FILLED),
        Coordinate(0, 2, max_value): Cell(CellValue(None, max_value), CellState.EMPTY),
        Coordinate(1, 0, max_value): Cell(CellValue(3, max_value), CellState.PRE_FILLED),
        Coordinate(1, 1, max_value): Cell(CellValue(4, max_value), CellState.PRE_FILLED),
        Coordinate(1, 2, max_value): Cell(CellValue(5, max_value), CellState.PRE_FILLED),
        Coordinate(2, 0, max_value): Cell(CellValue(6, max_value), CellState.PRE_FILLED),
        Coordinate(2, 1, max_value): Cell(CellValue(7, max_value), CellState.PRE_FILLED),
        Coordinate(2, 2, max_value): Cell(CellValue(8, max_value), CellState.PRE_FILLED),
    }
    grid = Grid.create(grid_size=9, cells=cells)  # Create a 9x9 grid to cover all cells
    print("Grid created successfully.")


if __name__ == "__main__":
    test_grid()
