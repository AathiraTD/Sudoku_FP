from enum import Enum


class CellState(Enum):
    PRE_FILLED = "pre_filled"  # The initial state of the cell
    USER_FILLED = "user_filled"  # The cell is filled with a value
    HINT = "hint"  # The cell is a hint
    EMPTY = "empty"  # The cell is empty
