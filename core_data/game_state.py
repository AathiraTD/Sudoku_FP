from typing import Dict, Tuple, List, Optional
from core_data.grid.grid import Grid


class GameState:
    def __new__(cls, grid: Grid, config: Dict, hints_used: int = 0, undo_stack: List[Tuple[int, int, int]] = None,
                redo_stack: List[Tuple[int, int, int]] = None):
        instance = super(GameState, cls).__new__(cls)
        instance.grid = grid
        instance.config = config
        instance.hints_used = hints_used
        instance.undo_stack = undo_stack if undo_stack is not None else []
        instance.redo_stack = redo_stack if redo_stack is not None else []
        return instance

    def increment_hints(self) -> 'GameState':
        return GameState(self.grid, self.config, self.hints_used + 1, self.undo_stack, self.redo_stack)

    def reset_hints(self) -> 'GameState':
        return GameState(self.grid, self.config, 0, self.undo_stack, self.redo_stack)

    def hints_remaining(self) -> int:
        return self.config['hint_limit'] - self.hints_used

    def can_use_hint(self) -> bool:
        return self.hints_used < self.config['hint_limit']

    def with_grid(self, grid: Grid) -> 'GameState':
        return GameState(grid, self.config, self.hints_used, self.undo_stack, self.redo_stack)

    def push_undo(self, action: Tuple[int, int, int]) -> 'GameState':
        new_undo_stack = self.undo_stack + [action]
        return GameState(self.grid, self.config, self.hints_used, new_undo_stack, self.redo_stack)

    def pop_undo(self) -> Tuple[Optional[Tuple[int, int, int]], 'GameState']:
        if not self.undo_stack:
            return None, self
        action = self.undo_stack[-1]
        new_undo_stack = self.undo_stack[:-1]
        return action, GameState(self.grid, self.config, self.hints_used, new_undo_stack, self.redo_stack)

    def push_redo(self, action: Tuple[int, int, int]) -> 'GameState':
        new_redo_stack = self.redo_stack + [action]
        return GameState(self.grid, self.config, self.hints_used, self.undo_stack, new_redo_stack)

    def pop_redo(self) -> Tuple[Optional[Tuple[int, int, int]], 'GameState']:
        if not self.redo_stack:
            return None, self
        action = self.redo_stack[-1]
        new_redo_stack = self.redo_stack[:-1]
        return action, GameState(self.grid, self.config, self.hints_used, self.undo_stack, new_redo_stack)

    def clear_redo(self) -> 'GameState':
        return GameState(self.grid, self.config, self.hints_used, self.undo_stack, [])
