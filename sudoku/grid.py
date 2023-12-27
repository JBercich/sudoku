#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""Sudoku grid class."""

from __future__ import annotations

from typing import TypeAlias, Any

from sudoku.cell import Cell

GridMatrix: TypeAlias = list[list[Cell]]


class Grid:
    """Sudoku grid."""

    ROWS: int = 9
    COLS: int = 9

    @property
    def grid(self) -> int:
        """Grid property for overriding getter."""
        return self._grid

    @grid.getter
    def grid(self) -> GridMatrix:
        """Custom value getter to track the total grid accesses made."""
        self._get_count += 1
        return self._grid

    @grid.setter
    def grid(self, value: GridMatrix) -> GridMatrix:
        """Custom value setter for the grid property."""
        self._grid = value

    def __init__(self):
        self.grid: GridMatrix = self.init_empty_grid()
        self._get_count: int = 0

    def __getitem__(self, index: Any) -> Any:
        """Custom index dunder method for easy grid access when getting cell values."""
        if not (isinstance(index, (list, tuple, set)) and len(index) == 2):
            raise TypeError(f"Grid access with (row, column) indexing: {index}")
        return self.grid[index[0]][index[1]]

    def __setitem__(self, index: Any, value: Any) -> Any:
        """Custom index dunder method for easy grid access when setting cell values."""
        if not (isinstance(index, (list, tuple, set)) and len(index) == 2):
            raise TypeError(f"Grid access with (row, column) indexing: {index} {value}")
        self.grid[index[0]][index[1]].value = value

    def __str__(self) -> str:
        """Custom string dunder method for stdout."""
        return "\n".join([str(row).strip("[]").replace(",", "") for row in self.grid])

    def __repr__(self) -> str:
        """Custom representation dunder method for stdout."""
        return self.__str__()

    @classmethod
    def init_empty_grid(cls) -> GridMatrix:
        """Initialise an empty grid of cells set to a value of 0."""
        return [[Cell(value=0) for _ in range(cls.COLS)] for _ in range(cls.ROWS)]
