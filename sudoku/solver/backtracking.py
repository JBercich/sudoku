#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import numpy as np

from sudoku.solver.abc import Solver


class BackTrackingSolver(Solver):
    def setup(self, *args, **kwargs) -> bool:
        super().setup(*args, **kwargs)
        self.search_space: np.ndarray = self._setup_search_space()
        return False

    def solve(self, *args, **kwargs) -> bool:
        super().solve(*args, **kwargs)
        return self._backtrack(0, 0)

    def _setup_search_space(self) -> np.ndarray:
        shape: tuple[int, int, int] = (*self.sudoku.shape, self.sudoku.grid_size + 1)
        search_space: np.ndarray = np.zeros(shape, dtype=np.bool_)
        search_space[:, :, 1:] = 1
        return search_space

    def _backtrack(self, row: int = 0, col: int = 0) -> bool:
        # Base condition reaching beyond sudoku cell space
        if row == self.sudoku.grid_size:
            return True
        # Define update cells when reaching cell grid borders
        _col: int = col + 1 if col + 1 < self.sudoku.grid_size else 0
        _row: int = row + 1 if _col == 0 else row
        # Skip cells that are frozen without changing the value
        if self.sudoku.cells_frozen[row, col] != 0:
            return self._backtrack(_row, _col)
        # Iterate over cell index search space
        for (v,), valid_value_update in np.ndenumerate(self.search_space[row, col]):
            # Only update cell with values in search space
            if valid_value_update:
                self.sudoku.cells[row, col] = v
                # Recurse to next cell if update is valid
                if self.sudoku.cell_is_valid(row, col):
                    if self._backtrack(_row, _col):
                        return True
        # Recurse backwards if cell is incomplete
        self.sudoku.cells[row, col] = 0
        return False
