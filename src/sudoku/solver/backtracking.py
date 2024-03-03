#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""Backtracking solver class."""

import sys

from sudoku.grid import Cell, Grid
from sudoku.solver.solver import Solver

sys.tracebacklimit = 0


class BacktrackingSolver(Solver):
    """Backtracking solver class."""

    @classmethod
    def solve(cls, grid: Grid, search_all_values: bool = True, **params):
        cls._backtrack(
            grid=grid,
            row=0,
            col=0,
            search_all_values=search_all_values,
        )
        return grid

    @classmethod
    def _backtrack(
        cls, grid: Grid, row: int, col: int, search_all_values: bool
    ) -> bool:
        """Recursive solver method using backtracking."""

        # Perform base-case check of reaching out of bounds index, find next indicies
        if row >= grid.get_grid_size() or col >= grid.get_grid_size():
            return True
        next_col: int = col + 1 if col < grid.max_value - 1 else 0
        next_row: int = row + 1 if next_col == 0 else row

        # Skip the cell if it is a static fixed cell
        if grid[row, col].static:
            return cls._backtrack(grid, next_row, next_col, search_all_values)

        lower_bound: int = 0 if not search_all_values else grid[row, col].value + 1
        for next_value in range(lower_bound, grid.max_value + 1):
            if cls.validate_update(grid, row, col, next_value):
                grid[row, col] = next_value
                is_solved: bool = cls._backtrack(
                    grid, next_row, next_col, search_all_values
                )
                if is_solved:
                    return True
        grid[row, col].set_empty_value()
        return False

    # Update validation
    # -----------------
    # When performing individual updates of a cell during backtracking, reducing update
    # cell sets and gets will minimise the overall runtime complexity. This section does
    # not perform full grid validation, it will only validate the row, column and grid
    # of the current cell being updated.

    @classmethod
    def validate_update(cls, grid: Grid, row: int, col: int, value: int) -> bool:
        """Validate a cell update for the sudoku grid."""
        row_upd: bool = cls.validate_row_update(grid, row, value)
        col_upd: bool = cls.validate_col_update(grid, col, value)
        grid_upd: bool = cls.validate_grid_update(grid, row, col, value)
        return row_upd and col_upd and grid_upd

    @classmethod
    def validate_row_update(cls, grid: Grid, row: int, value: int) -> bool:
        """Validate a row update with a value at some index upholds constraints."""
        return value not in [cell.value for cell in grid.get_row(row)]

    @classmethod
    def validate_col_update(cls, grid: Grid, col: int, value: int) -> bool:
        """Validate a column update with a value at some index upholds constraints."""
        return value not in [cell.value for cell in grid.get_column(col)]

    @classmethod
    def validate_grid_update(cls, grid: Grid, row: int, col: int, value: int) -> bool:
        """Validate a grid update with a value at some index upholds constraints."""
        return value not in [cell.value for cell in grid.get_subgrid(row, col)]
