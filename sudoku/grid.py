#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""Sudoku grid class."""

from __future__ import annotations

import re
from collections import Counter
from typing import Any, TypeAlias

from sudoku.cell import Cell

GridMatrix: TypeAlias = list[list[Cell]]


class Grid:
    """Sudoku grid."""

    ROWS: int = 9
    COLS: int = 9
    GRID: int = 9
    GRID_LEN: int = 3

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

    def get_row(self, row: int) -> list[Cell]:
        """Getter for a row of cells."""
        return self.grid[row]

    def get_col(self, col: int) -> list[Cell]:
        """Getter for a column of cells."""
        return [row[col] for row in self.grid]

    def get_grid(self, row: int, col: int) -> list[Cell]:
        """Getter for a sub-grid of cells."""
        return [
            self[row, col]
            for row, col in [
                (
                    r + (row // Grid.GRID_LEN) * Grid.GRID_LEN,
                    c + (col // Grid.GRID_LEN) * Grid.GRID_LEN,
                )
                for r in range(Grid.GRID_LEN)
                for c in range(Grid.GRID_LEN)
            ]
        ]

    @classmethod
    def init_empty_grid(cls) -> GridMatrix:
        """Initialise an empty grid of cells set to a value of 0."""
        return [[Cell(value=0) for _ in range(cls.COLS)] for _ in range(cls.ROWS)]

    def validate(self) -> bool:
        """Validate a grid upholds all rule constraints."""

        # Generate counters for rows, columns and small grids
        counters: list[Counter] = []
        for i in range(self.ROWS):
            counters.append(Counter([cell.value for cell in self.grid[i]]))
        for i in range(self.COLS):
            counters.append(Counter([row[i].value for row in self.grid]))
        for i in range(self.GRID):
            offset_row: int = (i // self.GRID_LEN) * self.GRID_LEN
            offset_col: int = (i % self.GRID_LEN) * self.GRID_LEN
            indicies: list[int] = [
                (row + offset_row, col + offset_col)
                for row in range(self.GRID_LEN)
                for col in range(self.GRID_LEN)
            ]
            counters.append(Counter([self[ind].value for ind in indicies]))

        # Check if any counter breaches the constraints
        for counter in counters:
            for value, count in counter.items():
                if value != Cell._MIN and count > Cell._MIN + 1:
                    return False
        return True

    @classmethod
    def load_string(cls, grid_string: str, post_validate: bool = True) -> Grid:
        """Load in a sudoku grid from a string of cell values."""

        # Validate the grid string
        if re.fullmatch(r"[0-9].{0,81}", grid_string) is None:
            raise ValueError(f"Invalid grid string format: {grid_string}")

        # Create a new board and load each value
        grid: Grid = Grid()
        index: int = 0
        for row in range(cls.ROWS):
            for col in range(cls.COLS):
                grid[row, col] = int(grid_string[index])
                if int(grid_string[index]) != Cell._MIN:
                    grid[row, col].static = True
                index += 1

        # Validate the loaded string
        if post_validate and not grid.validate():
            raise ValueError(f"Loaded sudoku board is not valid: {grid_string}")

        # Reset cell counters
        for row in range(cls.ROWS):
            for col in range(cls.COLS):
                grid[row, col].reset_counters()

        return grid

    def dump_string(self) -> str:
        """Dump the grid as a single string sequence of cell values."""
        grid: str = ""
        for row in self.grid:
            grid += "".join([str(cell.value) for cell in row])
        return grid
