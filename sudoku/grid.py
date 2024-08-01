#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import math
from typing import Any

from sudoku.exceptions import GridException


class Grid:
    MISSING: int = 0
    MIN_DIM: int = 1
    MIN_LEN: int = 1
    MAX_DIM: int = 5
    MAX_LEN: int = 625

    def __init__(self, grid: Any):
        self.values: list[int] = self._init_values(grid)
        self.frozen: list[int] = self._init_frozen(self.values)
        self.dim_sq: int = self._init_dim_sq(self.values)
        self.dim_bx: int = int(self.dim_sq**2)

    @classmethod
    def _parse_str_grid(cls, grid: str) -> list[int]:
        if not (grid := grid.strip()).isdigit():
            raise GridException(f"Unable to build input grid: {grid}")
        return [int(x) for x in grid.strip()]

    @classmethod
    def _parse_int_grid(cls, grid: int) -> list[int]:
        return cls._parse_str_grid(str(grid))

    @classmethod
    def _parse_list_grid(cls, grid: list[Any]) -> list[int]:
        if any([not isinstance(x, (str, int)) for x in grid]):
            raise GridException(f"Grid has invalid types: {grid}")
        elif any([not str(x).isdigit() for x in grid]):
            raise GridException(f"Grid has invalid values: {grid}")
        return [int(x) for x in grid]

    @classmethod
    def _init_values(cls, grid: Any) -> list[int]:
        match grid:
            case str():
                return cls._parse_str_grid(grid)
            case int():
                return cls._parse_int_grid(grid)
            case list():
                return cls._parse_list_grid(grid)
            case _:
                raise GridException(f"Grid has invalid type: {grid}")

    @classmethod
    def _init_frozen(cls, values: list[int]) -> list[int]:
        return [int(x != cls.MISSING) for x in values]

    @classmethod
    def _init_dim_sq(cls, values: list[int]) -> int:
        if (num_values := len(values)) > cls.MAX_LEN:
            raise GridException(f"Grid is too large: {num_values}")
        if num_values < cls.MIN_LEN:
            raise GridException(f"Grid is too small: {num_values}")
        dim_bx: float = math.sqrt(num_values)
        dim_sq: float = math.sqrt(int(dim_bx))
        if dim_sq != (dim := int(dim_sq)):
            raise GridException(f"Grid is non-square: {dim} x `{dim}")
        return dim
