from typing import List

from colorama import Fore, Style

from core_data.cell_state import CellState
from core_data.grid.grid import Grid


def print_column_labels(grid_size: int, subgrid_size: int):
    """
    Function to print the column labels using recursion.
    """
    def _print_column_labels(col_index: int):
        if col_index >= grid_size:
            print()
            return  # Base case: all column labels have been printed
        if col_index == 0:
            print("    ", end="")
        if col_index > 0 and col_index % subgrid_size == 0:
            print("  ", end="")  # Add space for separator
        print(f" {col_index + 1}  ", end="")
        _print_column_labels(col_index + 1)  # Recursive call to print the next column label

    _print_column_labels(0)

def display_grid(grid: Grid):
    """
    Function to display the Sudoku grid with row and column labels using recursion.
    """
    grid_size = grid.grid_size
    subgrid_size = int(grid_size ** 0.5)

    print(
        f"\n(See your Sudoku Puzzle. Pre-Filled in {Fore.GREEN}Green{Style.RESET_ALL}, User-Filled in {Fore.BLUE}Blue{Style.RESET_ALL}, and Hint in {Fore.YELLOW}Yellow{Style.RESET_ALL})")

    def print_all_rows(row_index: int):
        """
        Recursively print all rows of the Sudoku grid.
        """
        if row_index >= grid_size:
            return  # Base case: all rows have been printed
        if row_index % subgrid_size == 0 or row_index == 0:
            print("   " + "-" * (4 * grid_size + subgrid_size + 1))  # Print the horizontal separator
        print_row(grid, row_index)  # Print the current row
        print_all_rows(row_index + 1)  # Recursive call to print the next row

    print_column_labels(grid_size, subgrid_size)  # Print the column labels
    print_all_rows(0)  # Start the recursion for rows
    print("   " + "-" * (4 * grid_size + subgrid_size + 1))  # Print the bottom boundary

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

        cell = grid[row_index, col_index]
        if cell is not None and cell.value.value is not None:
            value_str = str(cell.value.value)
            if cell.state == CellState.PRE_FILLED:
                row_display.append(Fore.GREEN + f" {value_str} " + Style.RESET_ALL)
            elif cell.state == CellState.USER_FILLED:
                row_display.append(Fore.BLUE + f" {value_str} " + Style.RESET_ALL)
            elif cell.state == CellState.HINT:
                row_display.append(Fore.YELLOW + f" {value_str} " + Style.RESET_ALL)
            else:
                row_display.append(f" {value_str} ")
        else:
            row_display.append(" . ")

        if (col_index + 1) % subgrid_size == 0 and (col_index + 1) != grid_size:
            row_display.append("|")  # Add vertical separator for subgrids
        print_cell(col_index + 1)  # Recursive call to print the next cell

    print_cell(0)  # Start the recursion for columns

def display_messages(messages: List[str], index: int = 0):
    """
    Recursively display messages.
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
