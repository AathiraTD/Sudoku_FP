from enum import Enum

class CellState(Enum):
    INITIAL = "initial"  # The initial state of the cell
    FILLED = "filled"  # The cell is filled with a value
    HINT = "hint"  # The cell is a hint
    EMPTY = "empty"  # The cell is empty
