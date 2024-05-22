from typing import List
from colorama import Fore, Style

from core_data.coordinate import Coordinate
from core_data.grid.grid import Grid
from core_data.cell_state import CellState

def print_column_labels(grid_size: int, subgrid_size: int):
    """
    Function to print the column labels using recursion.
    """

    def _print_column_labels(col_index: int):
        if col_index >= grid_size:
            print()
            return  # Base case: all column labels have been printed
        if col_index == 0:
            print("   ", end="")

        if col_index > 0 and col_index % subgrid_size == 0:
            print(" ", end=" ")  # Add space for separator
        print(f" {col_index + 1}", end="")

        # Recursive call to print the next column label
        _print_column_labels(col_index + 1)

    _print_column_labels(0)


def display_grid(grid: Grid):
    """
    Function to display the Sudoku grid with row and column labels using recursion.
    """

    # Retrieve the size of the grid and the size of subgrids
    grid_size = grid.grid_size
    subgrid_size = int(grid_size ** 0.5)

    def print_all_rows(row_index: int):
        """
        Recursively print all rows of the Sudoku grid.

        Args:
            row_index (int): The current row index to print.
        """
        if row_index >= grid_size:
            print(f"\n(See your Sudoku Puzzle. Pre-Filled in {Fore.GREEN}Green{Style.RESET_ALL}, User-Filled in {Fore.BLUE}Blue{Style.RESET_ALL}, and Hint in {Fore.YELLOW}Yellow{Style.RESET_ALL})")
            return  # Base case: all rows have been printed

        # Print the horizontal separator for subgrids and outer boundaries
        if row_index % subgrid_size == 0 or row_index == 0:
            print("   " + "-" * (2 * grid_size + subgrid_size + 1))

        # Print the current row with separators
        print_row(grid, row_index)

        # Recursive call to print the next row
        print_all_rows(row_index + 1)

    # Print the column labels
    print_column_labels(grid_size, subgrid_size)

    # Start the recursion for rows
    print_all_rows(0)

    # Print the bottom boundary
    print("   " + "-" * (2 * grid_size + subgrid_size + 1))


def print_row(grid: Grid, row_index: int):
    """
    Recursively prints the cells of a given row with color-coding for different cell states.
    """
    grid_size = grid.grid_size
    subgrid_size = int(grid_size ** 0.5)
    row_label = get_row_label(row_index)
    row_display = [row_label + " |"]

    def print_cell(col_index: int):
        if col_index >= grid_size:
            row_display.append("|")
            print(" ".join(row_display))
            return  # Base case: all columns in the current row have been printed

        coord = Coordinate(row_index, col_index, grid_size)
        cell = grid.cells.get(coord)
        if cell is not None and cell.value.value is not None:
            value_str = str(cell.value.value)
            if cell.state == CellState.PRE_FILLED:
                row_display.append(Fore.GREEN + value_str + Style.RESET_ALL)
            elif cell.state == CellState.USER_FILLED:
                row_display.append(Fore.BLUE + value_str + Style.RESET_ALL)
            elif cell.state == CellState.HINT:
                row_display.append(Fore.YELLOW + value_str + Style.RESET_ALL)
            else:
                row_display.append(value_str)
        else:
            row_display.append(".")

        # Add vertical separator for subgrids
        if (col_index + 1) % subgrid_size == 0 and (col_index + 1) != grid_size:
            row_display.append("|")

        # Recursive call to print the next cell
        print_cell(col_index + 1)

    # Start the recursion for columns
    print_cell(0)


def display_messages(messages: List[str], index: int = 0):
    """
    Recursively display messages.

    Args:
        messages (List[str]): The list of messages to display.
        index (int, optional): The current index of the message to display. Defaults to 0.
    """
    if index >= len(messages):  # Base case: all messages have been displayed
        return
    print(messages[index])
    display_messages(messages, index + 1)  # Recursively display the next message


def get_row_label(index: int) -> str:
    """
    Convert a row index to a row label (A, B, C, etc.).
    """
    return chr(ord('A') + index)
