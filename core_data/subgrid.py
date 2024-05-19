from dataclasses import dataclass
from typing import Tuple
from .cell import Cell


@dataclass(frozen=True)
class Subgrid:
    cells: Tuple[Cell, ...]
    subgrid_index: int

    def __new__(cls, cells: Tuple[Cell, ...], subgrid_index: int):
        if not cls.is_valid(cells):
            raise ValueError("All elements of the subgrid must be instances of Cell.")
        instance = super().__new__(cls)
        object.__setattr__(instance, 'cells', cells)
        object.__setattr__(instance, 'subgrid_index', subgrid_index)
        return instance

    @staticmethod
    def is_valid(cells: Tuple[Cell, ...]) -> bool:
        return all(isinstance(cell, Cell) for cell in cells)

    @staticmethod
    def create(cells: Tuple[Cell, ...], subgrid_index: int):
        try:
            return Subgrid(cells, subgrid_index)
        except ValueError as e:
            print(e)
            return None
