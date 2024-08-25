#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import numpy as np

from pydoku.solver.abc import Solver


class BackTrackingSolver(Solver):
    def setup(self, *args, **kwargs) -> bool:
        super().setup(*args, **kwargs)
        self.search_space: np.ndarray = self._setup_search_space()
        self._reduce_search_space()
        self.search_order: np.ndarray = self._setup_search_order()
        return False

    def solve(self, *args, **kwargs) -> bool:
        super().solve(*args, **kwargs)
        return self._backtrack(0)

    def _setup_search_space(self) -> np.ndarray:
        shape: tuple[int, int, int] = (*self.sudoku.shape, self.sudoku.grid_size + 1)
        search_space: np.ndarray = np.zeros(shape, dtype=np.bool_)
        search_space[:, :, 1:] = 1
        return search_space

    def _setup_search_order(self, sort_by_size: bool = True) -> np.ndarray:
        search_counts: np.ndarray = np.apply_along_axis(np.sum, 2, self.search_space)
        search_idxs: np.ndarray = np.indices(search_counts.shape)
        search_space: np.ndarray = np.stack([search_idxs[0], search_idxs[1]], axis=-1)
        if sort_by_size:
            _sorted: np.ndarray = np.argsort(search_counts, axis=None, kind="mergesort")
            return search_space.reshape((search_counts.size, 2))[_sorted]
        return search_space.reshape((search_counts.size, 2))

    def _reduce_search_space(self) -> np.ndarray:
        for idx in range(self.sudoku.grid_size):
            row: np.ndarray = np.unique(self.sudoku.get_row_by_idx(idx))
            col: np.ndarray = np.unique(self.sudoku.get_col_by_idx(idx))
            box: np.ndarray = np.unique(self.sudoku.get_box_by_num(idx).reshape(-1))
            d: int = self.sudoku.box_size
            i: int = idx // d * d
            j: int = idx % d * d
            self.search_space[idx, :, row] = False
            self.search_space[:, idx, col] = False
            self.search_space[i : i + d, j : j + d, box] = False

        return self.search_space

    def _backtrack(self, idx: int = 0) -> bool:
        # Base condition reaching beyond sudoku cell space
        if idx == self.sudoku.cells.size:
            return True
        # Pull search indicies for current cell
        row: int = self.search_order[idx][0]
        col: int = self.search_order[idx][1]
        # Skip cells that are frozen without changing the value
        if self.sudoku.cells_frozen[row, col] != 0:
            return self._backtrack(idx + 1)
        # Iterate over cell index search space
        for (v,), valid_value_update in np.ndenumerate(self.search_space[row, col]):
            # Only update cell with values in search space
            if valid_value_update:
                self.sudoku.cells[row, col] = v
                # Recurse to next cell if update is valid
                if self.sudoku.cell_is_valid(row, col):
                    if self._backtrack(idx + 1):
                        return True
        # Recurse backwards if cell is incomplete
        self.sudoku.cells[row, col] = 0
        return False
