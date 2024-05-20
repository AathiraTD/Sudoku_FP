from typing import List, Optional, Tuple, Set
import math
import random

from core_data.cell_state import CellState
from core_data.coordinate import Coordinate
from core_data.grid import Grid


# Finds the next empty cell in the Sudoku grid.
def find_empty_cell(grid: Grid, size: int) -> Optional[Tuple[int, int]]:
    def find_cell(row: int, col: int) -> Optional[Tuple[int, int]]:
        if row >= size:  # Base case: No more rows
            return None
        if col >= size:  # Move to the next row if col exceeds size
            return find_cell(row + 1, 0)
        cell = grid.get(Coordinate(row, col))  # Get the cell at (row, col)
        if cell is None or cell[0].value == 0:  # Check if cell is empty
            return row, col
        return find_cell(row, col + 1)  # Recursively check the next cell

    return find_cell(0, 0)


# Validates if placing a number is valid according to Sudoku rules.
def is_valid(grid: Grid, row: int, col: int, num: int, size: int) -> bool:
    subgrid_size = int(math.sqrt(size))

    def in_row(r: int, c: int) -> bool:
        if c >= size:  # Base case: No more columns
            return False
        cell = grid.get(Coordinate(r, c))
        if cell and cell[0].value == num:  # Check if the number is in the row
            return True
        return in_row(r, c + 1)  # Recursively check the next column

    def in_col(r: int, c: int) -> bool:
        if r >= size:  # Base case: No more rows
            return False
        cell = grid.get(Coordinate(r, c))
        if cell and cell[0].value == num:  # Check if the number is in the column
            return True
        return in_col(r + 1, c)  # Recursively check the next row

    def in_subgrid(start_row: int, start_col: int, r: int, c: int) -> bool:
        if r >= start_row + subgrid_size:  # Base case: No more rows in subgrid
            return False
        if c >= start_col + subgrid_size:  # Move to the next row in subgrid
            return in_subgrid(start_row, start_col, r + 1, start_col)
        cell = grid.get(Coordinate(r, c))
        if cell and cell[0].value == num:  # Check if the number is in the subgrid
            return True
        return in_subgrid(start_row, start_col, r, c + 1)  # Recursively check the next cell in subgrid

    start_row, start_col = (row // subgrid_size) * subgrid_size, (col // subgrid_size) * subgrid_size
    return not in_row(row, 0) and not in_col(0, col) and not in_subgrid(start_row, start_col, start_row, start_col)


# Recursively applies the backtracking algorithm to solve the Sudoku grid.
def backtrack(grid: Grid, size: int) -> Tuple[Grid, bool]:
    empty_cell = find_empty_cell(grid, size)
    if not empty_cell:  # Base case: No empty cell found
        return grid, True

    row, col = empty_cell
    random_values = list(range(1, size + 1))
    random.shuffle(random_values)

    def try_values(values: List[int], grid: Grid) -> Tuple[Grid, bool]:
        if not values:  # Base case: No values left to try
            return grid, False
        value = values[0]
        if is_valid(grid, row, col, value, size):  # Check if value is valid
            new_grid = update_cell(grid, Coordinate(row, col), value, CellState.MUTABLE)
            new_grid, success = backtrack(new_grid, size)
            if success:  # If successful, return the new grid
                return new_grid, True
            new_grid = update_cell(new_grid, Coordinate(row, col), 0, CellState.MUTABLE)
        return try_values(values[1:], grid)  # Recursively try the next value

    return try_values(random_values, grid)


# Recursively counts the number of solutions for the given Sudoku grid.
def count_solutions(grid: Grid, size: int, max_solutions: int = 2) -> int:
    empty_cell = find_empty_cell(grid, size)
    if not empty_cell:  # Base case: No empty cell found
        return 1

    row, col = empty_cell
    num_solutions = 0

    def count_values(num: int) -> int:
        nonlocal num_solutions
        if num > size:  # Base case: No more values to check
            return num_solutions
        if is_valid(grid, row, col, num, size):
            new_grid = update_cell(grid, Coordinate(row, col), num, CellState.MUTABLE)
            num_solutions += count_solutions(new_grid, size, max_solutions)
            if num_solutions >= max_solutions:
                return num_solutions
        return count_values(num + 1)  # Recursively check the next value

    return count_values(1)


# Recursively removes cells from the grid based on the specified difficulty level.
def remove_cells_recursive(cells_to_remove: Set[Tuple[int, int]], grid: Grid, size: int) -> Grid:
    if not cells_to_remove:  # Base case: No more cells to remove
        return grid
    row, col = cells_to_remove.pop()
    new_grid = update_cell(grid, Coordinate(row, col), 0, CellState.MUTABLE)
    if count_solutions(new_grid, size) == 1:  # Ensure the puzzle remains uniquely solvable
        return remove_cells_recursive(cells_to_remove, new_grid, size)
    else:
        return remove_cells_recursive(cells_to_remove, grid, size)


# Generates a set of all cells in the grid.
def generate_all_cells(row: int, col: int, acc: Set[Tuple[int, int]], size: int) -> Set[Tuple[int, int]]:
    if row >= size:  # Base case: No more rows
        return acc
    if col >= size:  # Move to the next row if col exceeds size
        return generate_all_cells(row + 1, 0, acc, size)
    acc.add((row, col))  # Add the current cell to the accumulator
    return generate_all_cells(row, col + 1, acc, size)  # Recursively add the next cell


# Retrieves the possible values for a cell based on its row.
def get_possible_values(row: int, col: int, possible_values: Set[int], grid: Grid, size: int) -> Set[int]:
    if col >= size:  # Base case: No more columns
        return possible_values
    cell = grid.get(Coordinate(row, col))
    if cell:
        possible_values.discard(cell[0].value)  # Remove the value from possible values if it's already used
    return get_possible_values(row, col + 1, possible_values, grid, size)


# Retrieves the possible values for a cell based on its column.
def get_column_possible_values(row: int, col: int, possible_values: Set[int], grid: Grid, size: int) -> Set[int]:
    if row >= size:  # Base case: No more rows
        return possible_values
    cell = grid.get(Coordinate(row, col))
    if cell:
        possible_values.discard(cell[0].value)  # Remove the value from possible values if it's already used
    return get_column_possible_values(row + 1, col, possible_values, grid, size)


# Retrieves the possible values for a cell based on its subgrid.
def get_subgrid_possible_values(start_row: int, start_col: int, row: int, col: int, possible_values: Set[int],
                                grid: Grid, size: int) -> Set[int]:
    subgrid_size = int(math.sqrt(size))
    if row >= start_row + subgrid_size:  # Base case: No more rows in subgrid
        return possible_values
    if col >= start_col + subgrid_size:  # Move to the next row in subgrid
        return get_subgrid_possible_values(start_row, start_col, row + 1, start_col, possible_values, grid, size)
    cell = grid.get(Coordinate(row, col))
    if cell:
        possible_values.discard(cell[0].value)  # Remove the value from possible values if it's already used
    return get_subgrid_possible_values(start_row, start_col, row, col + 1, possible_values, grid, size)


# Applies the naked singles technique to the grid.
def apply_naked_singles(row: int, col: int, grid: Grid, size: int) -> Grid:
    if row >= size:  # Base case: No more rows
        return grid
    if col >= size:  # Move to the next row if col exceeds size
        return apply_naked_singles(row + 1, 0, grid, size)
    cell = grid.get(Coordinate(row, col))
    if cell and cell[0].value == 0:
        possible_values = set(range(1, size + 1))
        possible_values = get_possible_values(row, 0, possible_values, grid, size)
        possible_values = get_column_possible_values(0, col, possible_values, grid, size)
        start_row, start_col = (row // subgrid_size) * subgrid_size, (col // subgrid_size) * subgrid_size
        possible_values = get_subgrid_possible_values(start_row, start_col, start_row, start_col, possible_values, grid,
                                                      size)
        if len(possible_values) == 1:
            grid = update_cell(grid, Coordinate(row, col), list(possible_values)[0], CellState.MUTABLE)
    return apply_naked_singles(row, col + 1, grid, size)


# Generates a Sudoku puzzle based on the specified difficulty level.
def generate_puzzle(difficulty: str, grid: Grid, size: int) -> Optional[Grid]:
    try:
        print(f"Generating puzzle with difficulty {difficulty} and size {size}")
        grid, success = backtrack(grid, size)  # Use backtracking to generate a complete Sudoku
        if success:
            grid = apply_naked_singles(0, 0, grid, size)  # Apply naked singles technique
            all_cells = generate_all_cells(0, 0, set(), size)  # Generate all cells
            num_cells_to_remove = {
                "easy": size * size // 4,
                "medium": size * size // 3,
                "hard": size * size // 2
            }[difficulty.lower()]
            cells_to_remove = set(random.sample(sorted(all_cells), num_cells_to_remove))
            grid = remove_cells_recursive(cells_to_remove, grid, size)  # Remove cells based on difficulty
            if count_solutions(grid, size) == 1:  # Ensure the puzzle has a unique solution
                return grid
            else:
                print("Error: Generated puzzle does not have a unique solution!")
                return None
        else:
            print("Error: No solution found!")
            return None
    except Exception as e:
        print(f"Error in generating puzzle: {e}")
        return None
