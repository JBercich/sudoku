#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""Grid abstraction."""

from __future__ import annotations

import math
import re
from collections import Counter
from typing import Any, Final

from sudoku.cell import Cell

DEFAULT_GRID_SIZE: Final[int] = 9
MINIMUM_GRID_SIZE: Final[int] = 2
MAXIMUM_GRID_SIZE: Final[int] = 36


class Grid:
    """Sudoku grid.

    A grid contains `Cell` instances assorted in a matrix-like data structure composed
    of list rows. The grid size can be customised with an integral root grid width. Grid
    helper methods aim to minimise grid complexity by reducing required logical methods.

    Attributes:
        grid (list[list[Cell]]): Grid matrix data structure composed of Cell instances.
            Defaults to an empty grid with all cells filled with `EMPTY_CELL_VALUE`.
    """

    def __init__(self, size: int = DEFAULT_GRID_SIZE):
        if size < MINIMUM_GRID_SIZE or size > MAXIMUM_GRID_SIZE:
            raise ValueError(f"Invalid grid size: {size}")
        if not math.sqrt(size).is_integer():
            raise ValueError("Grid size must have integral root for valid grids.")
        self.grid: list[list[Cell]] = self._init_empty_grid(size)
        self._grid_size: int = size
        self._getter_counter: int = 0

    # grid
    # ----
    # Overloading the sudoku grid attribute prevents explicit setting of the grid with a
    # different value. Attribute access is allowed and has an attached counter to track
    # any extra metrics during a solver method.

    @property
    def grid(self) -> list[list[Cell]]:
        self._getter_counter += 1
        return self._grid

    @grid.setter
    def grid(self, value: Any) -> None:
        raise NotImplementedError("Cannot set grid attribute.")

    # Dunder methods
    # --------------
    # Builtin dunders are overloaded to simplify cell access by a (row, column) indexing
    # approach similar to numpy. This will also allow easy iteration over all cells in a
    # grid without accounting for indexing complexity.

    def __iter__(self):
        """Instance iteration method for LR-TB enumeration of cells."""
        cells: list[Cell] = []
        for row in self.grid:
            cells += row
        return cells

    def __getitem__(self, index: Any) -> Any:
        """Instance get-item method for (row, column) grid index getting."""
        if not (isinstance(index, (list, tuple)) and len(index) == 2):
            raise TypeError(f"Grid access with (row, column) indexing: {index}")
        return self.grid[index[0]][index[1]]

    def __setitem__(self, index: Any, value: Any) -> Any:
        """Instance get-item method for (row, column) grid index setting."""
        if not (isinstance(index, (list, tuple)) and len(index) == 2):
            raise TypeError(f"Grid access with (row, column) indexing: {index}")
        self.grid[index[0]][index[1]].value = value

    def __str__(self) -> str:
        """Instance string method for grid stdout."""
        return "\n".join([str(row).strip("[]").replace(",", "") for row in self.grid])

    # Helper methods
    # --------------
    # Additional helper methods are defined for accessing certain components of the grid
    # such as subfield ranges like a row or column or subgrid. Initialising an empty
    # instance an getting the sizes of the grid and subgrid are also defined for the
    # protected attribute.

    def get_grid_size(self) -> int:
        """Getter for the full grid size."""
        return len(self._grid_size)

    def get_subgrid_size(self) -> int:
        """Getter for the subgrid size."""
        return int(math.sqrt(self.get_grid_size()))

    def get_row(self, row: int) -> list[Cell]:
        """Getter for a row of cells."""
        return self.grid[row]

    def get_column(self, col: int) -> list[Cell]:
        """Getter for a column of cells."""
        return [row[col] for row in self.grid]

    def get_subgrid(self, row: int, col: int) -> list[Cell]:
        """Getter for a subgrid of cells."""
        size: int = self.get_subgrid_size()
        row_indicies: list[int] = [r + (row // size) * size for r in range(size)]
        col_indicies: list[int] = [c + (col // size) * size for c in range(size)]
        return [self[r, c] for r, c in zip(row_indicies, col_indicies)]

    @classmethod
    def _init_empty_grid(cls, size: int) -> list[list[Cell]]:
        """Initialise a grid matrix with all cells set as empty."""
        return [[Cell() for _ in range(size)] for _ in range(size)]

    def validate(self, complete: bool = False) -> bool:
        """Validate a grid upholds all rule constraints (and is complete)."""

        # Generate counters for rows, columns and small grids
        counters: list[Counter] = []
        for i in range(self.get_grid_size()):
            r: int = (i // self.get_subgrid_size()) * self.get_subgrid_size()
            c: int = (i % self.get_subgrid_size()) * self.get_subgrid_size()
            counters.append(Counter([cell for cell in self.get_row(i)]))
            counters.append(Counter([cell for cell in self.get_column(i)]))
            counters.append(Counter([cell for cell in self.get_subgrid(r, c)]))

        # Check if any counter breaches the constraints
        for counter in counters:
            for cell, count in counter.items():
                if cell.is_empty() and complete:
                    return False
                if not cell.is_empty() and count > 1:
                    return False
        return True

    # String representation
    # ---------------------
    # To simplify grid storage, a string representation is used for loading into a grid
    # instance and can be dumped to a string for easy correctness comparisons during any
    # testing methods.

    @classmethod
    def load_string(cls, grid_string: str, post_validate: bool = True) -> Grid:
        """Load a sudoku grid from a string into cell instances of a grid."""

        # Validate the grid string
        if re.fullmatch(r"[0-9].{0,81}", grid_string) is None:
            raise ValueError(f"Invalid grid string format: {grid_string}")

        # Create a new board and load each value
        grid: Grid = Grid()
        for cell, char in zip(grid, grid_string):
            is_static: bool = cell.value == int(char)
            cell.value = int(char)
            cell.static = True if is_static else cell.static

        # Validate the loaded string
        if post_validate and not grid.validate():
            raise ValueError(f"Loaded sudoku board is not valid: {grid_string}")

        # Reset cell counters
        for cell in grid:
            cell.reset_counters()
        return grid

    def dump_string(self) -> str:
        """Dump the grid as a single string sequence of cell values."""
        return "".join([str(cell.value) for cell in self])
