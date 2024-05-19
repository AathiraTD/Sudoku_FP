from dataclasses import dataclass
from typing import Tuple
from .cell import Cell

@dataclass(frozen=True)
class Grid:
    cells: Tuple[Tuple[Cell, ...], ...]
    grid_size: int

    def __new__(cls, cells: Tuple[Tuple[Cell, ...], ...], grid_size: int):
        if not cls.is_valid(cells, grid_size):
            raise ValueError(f"Grid must be {grid_size}x{grid_size}.")
        instance = super().__new__(cls)
        object.__setattr__(instance, 'cells', cells)
        object.__setattr__(instance, 'grid_size', grid_size)
        return instance

    @staticmethod
    def is_valid(cells: Tuple[Tuple[Cell, ...], ...], grid_size: int) -> bool:
        return len(cells) == grid_size and all(len(row) == grid_size for row in cells)

    @staticmethod
    def create(cells: Tuple[Tuple[Cell, ...], ...], grid_size: int):
        try:
            return Grid(cells, grid_size)
        except ValueError as e:
            print(e)
            return None
e