from dataclasses import dataclass
from typing import Dict, Optional, Tuple, Union, List
from types import MappingProxyType
from core_data.cell import Cell
from core_data.coordinate import Coordinate
from core_data.cell_state import CellState
from core_data.cell_value import CellValue
from utils.validation_utils import validate_grid
from .row import Row
from .column import Column
from .subgrid import Subgrid


@dataclass(frozen=True)
class Grid:
    """Represents a Sudoku grid with immutable cells and grid size."""
    cells: MappingProxyType  # An immutable dictionary of Coordinate keys and Cell values
    grid_size: int  # The size of the grid (e.g., 9 for a 9x9 grid)

    def __new__(cls, cells: Dict[Coordinate, Cell], grid_size: int, skip_validation: bool = False):
        """
        Create a new Grid instance with immutable cells.
        """
        # Convert the cells dictionary to an immutable MappingProxyType
        immutable_cells = MappingProxyType(cells)

        # Validate the cells before creating the instance
        if not skip_validation and not validate_grid(immutable_cells, grid_size):
            raise ValueError(
                f"Grid must be {grid_size}x{grid_size} with unique values in each row, column, and subgrid.")

        # Create a new instance using the superclass (__new__ method of object)
        instance = super(Grid, cls).__new__(cls)

        # Set the instance attributes cells and grid_size
        object.__setattr__(instance, 'cells', immutable_cells)
        object.__setattr__(instance, 'grid_size', grid_size)

        # Return the new instance
        return instance

    def __init__(self, cells: Dict[Coordinate, Cell], grid_size: int, skip_validation: bool = False):
        """
        Initialize a new Grid instance. This is a no-op since we handle initialization in __new__.
        This method is required to accept skip_validation to prevent TypeError.
        """
        pass

    def __getitem__(self, index: Union[int, Tuple[int, int], str]) -> Union[
        Row, Column, Subgrid, Cell, List[Row], List[Column], List[Subgrid]]:
        """
        Access different parts of the grid using various indices.
        """
        if isinstance(index, int):
            # Return a Row object for a single integer index
            return self.get_row(index)
        elif isinstance(index, tuple) and len(index) == 2:
            # Return the Cell object for a tuple index
            return self.cells[Coordinate(index[0], index[1], self.grid_size)]
        elif isinstance(index, str):
            if index == 'row':
                # Return a list of all Row objects
                return self.get_all_rows(0)
            elif index == 'column':
                # Return a list of all Column objects
                return self.get_all_columns(0)
            elif index == 'subgrid':
                # Return a list of all Subgrid objects
                return self.get_all_subgrids(0, 0, [])
        else:
            raise IndexError("Invalid index")

    @staticmethod
    def create(grid_size: int, cells: Optional[Dict[Coordinate, Cell]] = None, skip_validation: bool = False) -> "Grid":
        """
        Create a Grid instance, optionally with predefined cells.

        Args:
            grid_size (int): The size of the grid.
            cells (Optional[Dict[Coordinate, Cell]]): Predefined cells for the grid.
            skip_validation (bool): If True, skip the validation. Defaults to False.

        Returns:
            Grid: The created Grid instance.
        """
        if cells is None:
            cells = {}

            # Initialize all cells in the grid as empty using recursion
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

        # Return a new Grid instance with the provided or empty cells
        return Grid(cells=cells, grid_size=grid_size, skip_validation=skip_validation)

    def get_row(self, row_index: int) -> Row:
        """
        Get a Row object for a given row index.
        """
        row_cells = {coord: cell for coord, cell in self.cells.items() if coord.row_index == row_index}
        return Row(cells=row_cells, row_index=row_index, skip_validation=True)

    def get_column(self, column_index: int) -> Column:
        """
        Get a Column object for a given column index.
        """
        column_cells = {coord: cell for coord, cell in self.cells.items() if coord.col_index == column_index}
        return Column(cells=column_cells, column_index=column_index, skip_validation=True)

    def get_all_rows(self, index: int) -> List[Row]:
        """
        Recursively get a list of all Row objects.
        """
        # Base case: all rows have been added
        if index == self.grid_size:
            return []

        # Recursive call to get the next row and concatenate with the current row
        return [self.get_row(index)] + self.get_all_rows(index + 1)

    def get_all_columns(self, index: int) -> List[Column]:
        """
        Recursively get a list of all Column objects.
        """
        # Base case: all columns have been added
        if index == self.grid_size:
            return []

        # Recursive call to get the next column and concatenate with the current column
        return [self.get_column(index)] + self.get_all_columns(index + 1)

    def get_all_subgrids(self, row: int, col: int, subgrids: List[Subgrid]) -> List[Subgrid]:
        """
        Recursively get a list of all Subgrid objects.
        """
        subgrid_size = int(self.grid_size ** 0.5)

        # Base case: all subgrids have been added
        if row >= self.grid_size:
            return subgrids

        # Extract cells belonging to the current subgrid
        subgrid_cells = {
            coord: cell for coord, cell in self.cells.items()
            if row <= coord.row_index < row + subgrid_size and col <= coord.col_index < col + subgrid_size
        }

        # Calculate the subgrid index
        subgrid_index = (row // subgrid_size) * subgrid_size + (col // subgrid_size)

        # Create a Subgrid object and add it to the list
        subgrids.append(Subgrid(cells=subgrid_cells, subgrid_index=subgrid_index))

        # Calculate the next row and column indices for the next subgrid
        next_col = (col + subgrid_size) % self.grid_size
        next_row = row + subgrid_size if next_col == 0 else row

        # Recursive call to add the next subgrid
        return self.get_all_subgrids(next_row, next_col, subgrids)


def update_cell(grid: Grid, coordinate: Coordinate, value: Optional[int], state: CellState,
                skip_validation: bool = False) -> Grid:
    """
    Update a cell in the grid.

    Args:
        grid (Grid): The grid to update.
        coordinate (Coordinate): The coordinate of the cell to update.
        value (Optional[int]): The new value for the cell.
        state (CellState): The new state for the cell.
        skip_validation (bool): If True, skip validation. Defaults to False.

    Returns:
        Grid: The updated grid.
    """
    # Create a new dictionary of cells, copying the existing cells
    new_cells = dict(grid.cells)

    # Update the specific cell with the new value and state
    new_cells[coordinate] = Cell(CellValue(value, grid.grid_size), state)

    # Return a new Grid instance with the updated cells
    return Grid(cells=new_cells, grid_size=grid.grid_size, skip_validation=skip_validation)
