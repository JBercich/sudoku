#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import numpy as np


class Sudoku:
    MAX_ROW_LEN: int = 9
    MAX_COL_LEN: int = 9

    def __init__(self, grid_array: str):
        self.grid_search = np.array(list(grid_array), dtype=np.int8).reshape((9, 9))
        self.grid_static = np.copy(self.grid_search) != 0

    def _validate_row_constraint(self, row_idx: int) -> bool:
        row: np.ndarray = self.grid_search[row_idx, :]
        r_counter: dict = dict(zip(np.unique(row, return_counts=True)))
        if any([v > 1 for k, v in r_counter.items() if k != 0]):
            return False
        return True

    def _validate_col_constraint(self, col_idx: int) -> bool:
        col: np.ndarray = self.grid_search[:, col_idx]
        c_counter: dict = dict(zip(np.unique(col, return_counts=True)))
        if any([v > 1 for k, v in c_counter.items() if k != 0]):
            return False
        return True

    def _validate_grid(self) -> bool:
        pass

    # def naive_grid_validate(self) -> bool:
    #     counters: list[Counter] = []
    #     for i in range(self.get_grid_size()):
    #         r: int = (i // self.get_subgrid_size()) * self.get_subgrid_size()
    #         c: int = (i % self.get_subgrid_size()) * self.get_subgrid_size()
    #         counters.append(Counter([cell for cell in self.get_row(i)]))
    #         counters.append(Counter([cell for cell in self.get_column(i)]))
    #         counters.append(Counter([cell for cell in self.get_subgrid(r, c)]))
    #     for counter in counters:
    #         for v, count in counter.items():
    #             if not v != 0 and count > 1:
    #                 return False
    #     return True

    def _full_recursive_backtrack(self, row_idx: int, col_idx: int) -> bool:
        # Check if the final grid cell has been passed from recursion
        if row_idx >= self.MAX_ROW_LEN or col_idx >= self.MAX_COL_LEN:
            return True

        # Static cells are not processed, jump and return from next one
        new_col: int = col_idx + 1 if col_idx < self.MAX_COL_LEN - 1 else 0
        new_row: int = row_idx + 1 if new_col == 0 else row_idx
        if self.grid_static[row_idx, col_idx]:
            return self._recursive_backtrack(new_row, new_col)

        # Search all possible values for the cell as a "full" search
        for new_value in range(0, 9):
            for i in range(self.MAX_ROW_LEN):
                row = dict(zip(np.unique(self.grid_search[i, :], return_counts=True)))

            for i in range(self.MAX_COL_LEN):
                col = dict(zip(np.unique(self.grid_search[:, i], return_counts=True)))

            raise

            #     if cls.validate_update(grid, row_idx, col_idx, next_value):
            #         grid[row_idx, col_idx] = next_value
            #         is_solved: bool = _solve_backtrack(
            #             grid, next_row, next_col, search_all_values
            #         )
            #         if is_solved:
            #             return True
            # grid[row_idx, col_idx].set_empty_value()
            # return False


Sudoku(
    "000105006160800900390700501001907805050380060080000003070008659000000400008509207"
)._full_recursive_backtrack(0, 0)
# from sudoku.cell import DEFAULT_CELL_MINIMUM, Cell

# DEFAULT_GRID_SIZE: Final[int] = 9
# MINIMUM_GRID_SIZE: Final[int] = 2
# MAXIMUM_GRID_SIZE: Final[int] = 36


# class Grid:
#     """Sudoku grid.

#     A grid contains `Cell` instances assorted in a matrix-like data structure composed
#     of list rows. The grid size can be customised with an integral root grid width. Grid
#     helper methods aim to minimise grid complexity by reducing required logical methods.

#     Attributes:
#         grid (list[list[Cell]]): Grid matrix data structure composed of Cell instances.
#             Defaults to an empty grid with all cells filled with `EMPTY_CELL_VALUE`.
#     """

#     def __init__(self, size: int = DEFAULT_GRID_SIZE):
#         if size < MINIMUM_GRID_SIZE or size > MAXIMUM_GRID_SIZE:
#             raise ValueError(f"Invalid grid size: {size}")
#         if not math.sqrt(size).is_integer():
#             raise ValueError("Grid size must have integral root for valid grids.")
#         self.grid: list[list[Cell]] = self._init_empty_grid(size)
#         self.max_value: int = size
#         self.min_value: int = DEFAULT_CELL_MINIMUM
#         self._grid_size: int = size
#         self._getter_counter: int = 0

#     # grid
#     # ----
#     # Overloading the sudoku grid attribute has an attached counter to track any extra
#     # metrics about grid access during a solver method.

#     @property
#     def grid(self) -> list[list[Cell]]:
#         self._getter_counter += 1
#         return self._grid

#     @grid.setter
#     def grid(self, grid: Any) -> None:
#         self._grid = grid

#     # Dunder methods
#     # --------------
#     # Builtin dunders are overloaded to simplify cell access by a (row, column) indexing
#     # approach similar to numpy. This will also allow easy iteration over all cells in a
#     # grid without accounting for indexing complexity.

#     def __iter__(self):
#         """Instance iteration method for LR-TB enumeration of cells."""
#         cells: list[Cell] = []
#         for row in self.grid:
#             cells += row
#         return iter(cells)

#     def __getitem__(self, index: Any) -> Any:
#         """Instance get-item method for (row, column) grid index getting."""
#         if not (isinstance(index, (list, tuple)) and len(index) == 2):
#             raise TypeError(f"Grid access with (row, column) indexing: {index}")
#         return self.grid[index[0]][index[1]]

#     def __setitem__(self, index: Any, value: Any) -> Any:
#         """Instance get-item method for (row, column) grid index setting."""
#         if not (isinstance(index, (list, tuple)) and len(index) == 2):
#             raise TypeError(f"Grid access with (row, column) indexing: {index}")
#         self.grid[index[0]][index[1]].value = value

#     def __str__(self) -> str:
#         """Instance string method for grid stdout."""
#         return "\n".join([str(row).strip("[]").replace(",", "") for row in self.grid])

#     # Helper methods
#     # --------------
#     # Additional helper methods are defined for accessing certain components of the grid
#     # such as subfield ranges like a row or column or subgrid. Initialising an empty
#     # instance an getting the sizes of the grid and subgrid are also defined for the
#     # protected attribute.

#     def get_grid_size(self) -> int:
#         """Getter for the full grid size."""
#         return self._grid_size

#     def get_subgrid_size(self) -> int:
#         """Getter for the subgrid size."""
#         return int(math.sqrt(self.get_grid_size()))

#     def get_row(self, row: int) -> list[Cell]:
#         """Getter for a row of cells."""
#         return self.grid[row]

#     def get_column(self, col: int) -> list[Cell]:
#         """Getter for a column of cells."""
#         return [row[col] for row in self.grid]

#     def get_subgrid(self, row: int, col: int) -> list[Cell]:
#         """Getter for a subgrid of cells."""
#         size: int = self.get_subgrid_size()
#         row_indicies: list[int] = [r + (row // size) * size for r in range(size)]
#         col_indicies: list[int] = [c + (col // size) * size for c in range(size)]
#         return [self[r, c] for r, c in product(row_indicies, col_indicies)]

#     @classmethod
#     def _init_empty_grid(cls, size: int) -> list[list[Cell]]:
#         """Initialise a grid matrix with all cells set as empty."""
#         return [[Cell(maximum_value=size) for _ in range(size)] for _ in range(size)]

#     def validate(self, complete: bool = False) -> bool:
#         """Validate a grid upholds all rule constraints (and is complete)."""

#         # Generate counters for rows, columns and small grids
#         counters: list[Counter] = []
#         for i in range(self.get_grid_size()):
#             r: int = (i // self.get_subgrid_size()) * self.get_subgrid_size()
#             c: int = (i % self.get_subgrid_size()) * self.get_subgrid_size()
#             counters.append(Counter([cell for cell in self.get_row(i)]))
#             counters.append(Counter([cell for cell in self.get_column(i)]))
#             counters.append(Counter([cell for cell in self.get_subgrid(r, c)]))

#         # Check if any counter breaches the constraintss
#         for counter in counters:
#             for cell, count in counter.items():
#                 if cell.is_empty() and complete:
#                     return False
#                 if not cell.is_empty() and count > 1:
#                     return False
#         return True

#     # String representation
#     # ---------------------
#     # To simplify grid storage, a string representation is used for loading into a grid
#     # instance and can be dumped to a string for easy correctness comparisons during any
#     # testing methods.

#     @classmethod
#     def load_string(cls, grid_string: str, post_validate: bool = True) -> Grid:
#         """Load a sudoku grid from a string into cell instances of a grid."""

#         # Validate the grid string
#         if re.fullmatch(r"[0-9].{0,81}", grid_string) is None:
#             raise ValueError(f"Invalid grid string format: {grid_string}")

#         # Create a new board and load each value
#         grid: Grid = Grid()
#         for cell, char in zip(grid, grid_string):
#             cell.value = int(char)
#             cell.static = True if cell.value != 0 else cell.static

#         # Validate the loaded string
#         if post_validate and not grid.validate():
#             raise ValueError(f"Loaded sudoku board is not valid: {grid_string}")

#         # Reset cell counters
#         for cell in grid:
#             cell.reset_counters()
#         return grid

#     def dump_string(self) -> str:
#         """Dump the grid as a single string sequence of cell values."""
#         return "".join([str(cell.value) for cell in self])
