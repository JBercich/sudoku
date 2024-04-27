#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from enum import Enum, unique
from typing import TypeAlias, Literal

from sudoku_cli.sudoku import Grid
from sudoku_cli.sudoku.solvers.abc import Solver

UpdateValidator: TypeAlias = Literal["full", "changed"]


def _check_update_entire_grid(grid: Grid, *_, **__) -> bool:
    return grid.is_valid()


def _check_update_single_cell(grid: Grid, row_idx: int, col_idx: int, *_, **__) -> bool:
    return (
        grid.check_row_constraint(row_idx)
        and grid.check_col_constraint(col_idx)
        and grid.check_subgrid_constraint(row_idx, col_idx)
    )


def _lower_bounded_default(*_, **__) -> int:
    return 1


def _lower_bounded_smarter(grid: Grid, row_idx: int, col_idx: int, *_, **__) -> int:
    return grid.values[row_idx, col_idx] + 1


class BackTracking(Solver):
    name: str = "backtracking"

    @unique
    class UpdateMethod(Enum):
        entire_grid = _check_update_entire_grid
        single_cell = _check_update_single_cell

    @unique
    class LowerBounded(Enum):
        default_bound = _lower_bounded_default
        smarter_bound = _lower_bounded_smarter

    @classmethod
    def solve(
        cls,
        grid: Grid,
        update_method: UpdateMethod = UpdateMethod.single_cell,
        lower_bounded: LowerBounded = LowerBounded.default_bound,
    ) -> bool:
        def _backtrack(grid: Grid, row_idx: int, col_idx: int) -> bool:
            if row_idx >= 9 or col_idx >= 9:
                return True
            next_col: int = col_idx + 1 if col_idx < 8 else 0
            next_row: int = row_idx + 1 if next_col == 0 else row_idx

            if grid.frozen[row_idx, col_idx]:
                return _backtrack(grid, next_row, next_col)

            for next_value in range(lower_bounded(grid, row_idx, col_idx), 10):  # type: ignore
                grid.values[row_idx, col_idx] = next_value
                if update_method(grid, row_idx, col_idx):  # type: ignore
                    if _backtrack(grid, next_row, next_col):
                        return True
            grid.values[row_idx, col_idx] = 0
            return False

        return _backtrack(grid, 0, 0)
