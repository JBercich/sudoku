#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from collections import Counter

from sudoku.grid.grid import Grid


class Validator:
    @classmethod
    def is_valid(cls, grid: Grid) -> bool:
        for i in range(grid.dim_sq**2):
            if not cls.check_row_constraint(grid, i):
                return False
        for i in range(grid.dim_sq**2):
            if not cls.check_col_constraint(grid, i):
                return False
        for i in range(grid.dim_sq**2):
            if not cls.check_box_constraint(grid, i):
                return False
        return True

    @classmethod
    def is_complete(cls, grid: Grid) -> bool:
        return grid.MISSING not in grid.values and cls.is_valid(grid)

    @staticmethod
    def check_row_constraint(grid: Grid, row: int) -> bool:
        i: int = row * grid.dim_bx
        cntr: Counter = Counter(grid.values[i : i + grid.dim_bx])
        return all([j <= 1 for i, j in cntr.items() if i != grid.MISSING])

    @staticmethod
    def check_col_constraint(grid: Grid, col: int) -> bool:
        cntr: Counter = Counter(grid.values[col :: grid.dim_bx])
        return all([j <= 1 for i, j in cntr.items() if i != grid.MISSING])

    @staticmethod
    def check_box_constraint(grid: Grid, box: int) -> bool:
        cntr: Counter = Counter()
        col_offset: int = box % grid.dim_sq * grid.dim_sq
        row_offset: int = box // grid.dim_sq * grid.dim_sq
        for offset in range(grid.dim_sq):
            i: int = (row_offset + offset) * grid.dim_bx + col_offset
            cntr.update(grid.values[i : i + grid.dim_sq])
        return all([j <= 1 for i, j in cntr.items() if i != grid.MISSING])
