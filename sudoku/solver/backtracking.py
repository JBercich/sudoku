#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from sudoku.grid import Grid, Validator
from sudoku.solver.abc import Solver


class BackTrackingSolver(Solver):
    @classmethod
    def _backtrack(cls, grid: Grid, idx: int, vldr: Validator) -> bool:
        if idx >= len(grid.values):
            return True
        if grid.frozen[idx]:
            return cls._backtrack(grid, idx + 1, vldr)
        for value in range(max(1, grid.values[idx]), grid.dim_bx + 1):
            grid.values[idx] = value
            row: int = idx // grid.dim_bx
            col: int = idx % grid.dim_bx
            box: int = (row // grid.dim_sq) * grid.dim_sq + col // grid.dim_sq
            if (
                vldr.check_row_constraint(grid, row)
                and vldr.check_col_constraint(grid, col)
                and vldr.check_box_constraint(grid, box)
            ):
                if cls._backtrack(grid, idx + 1, vldr):
                    return True
        grid.values[idx] = 0
        return False

    def solve(self) -> bool:
        return self._backtrack(self.grid, 0, self.validator)
