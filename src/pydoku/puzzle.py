#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import abc
import math
from typing import Any


class Puzzle(abc.ABC):
    MISSING: int = 0

    def __init__(self, puzzle: Any):
        self.puzzle: Any = self._init_puzzle(puzzle)
        self.frozen: Any = self._init_frozen(self.puzzle)
        if not math.sqrt(num_cells := len(puzzle)).is_integer():
            raise ValueError(f"Puzzle has invalid number of cells: {num_cells}")
        self.pzl_dim: int = int(num_cells)  # Puzzle edge
        self.box_dim: int = int(math.sqrt(self.pzl_dim))  # Box edge

    @classmethod
    @abc.abstractmethod
    def _init_puzzle(cls, puzzle: Any) -> Any:
        pass

    @classmethod
    @abc.abstractmethod
    def _init_frozen(cls, puzzle: Any) -> Any:
        pass


# import itertools

# # import numpy as np

# # MISSING_CELL: int = 0
# puzzle_grid_size = 9
# puzzle_subsquare_size = 3


# def _generate_row_idxs(dim: int) -> list[int]:
#     """Generate row numbers per index given by cell dimensions."""
#     return list(itertools.chain(*[itertools.repeat(x, dim**2) for x in range(dim**2)]))


# def _generate_col_idxs(cell_dim: int) -> list[int]:
#     """Generate col numbers per index given by cell dimensions."""
#     return list(itertools.chain(*itertools.repeat(range(cell_dim**2), cell_dim**2)))

#     # def _generate_box_idxs(cell_dim: int) -> list[int]:
#     #     """Generate box numbers per index given by cell dimensions."""
#     #     rows: list[list[int]] = []
#     #     for x in range(cell_dim):
#     #         rows.extend(x)
#     #     return rows

#     return list(
#         itertools.chain(*[itertools.repeat(x, cell_dim) for x in range(cell_dim)])
#     )


# #     def __str__(self) -> str:
# #         s = ""
# #         for i in range(self.dim_bx):
# #             s += " ".join(
# #                 [
# #                     str(x)
# #                     for x in self.values[i * self.dim_bx : i * self.dim_bx + self.dim_bx]
# #                 ]
# #             )
# #             s += "\n"
# #         return s

# #     @classmethod
# #     def _parse_str_grid(cls, grid: str) -> GridArray:
# #         if not (grid := grid.strip()).isdigit():
# #             raise GridException(f"Unable to build input grid: {grid}")
# #         return [int(x) for x in grid.strip()]

# #     @classmethod
# #     def _parse_int_grid(cls, grid: int) -> GridArray:
# #         return cls._parse_str_grid(str(grid))

# #     @classmethod
# #     def _parse_list_grid(cls, grid: list[Any]) -> GridArray:
# #         if any([not isinstance(x, (str, int)) for x in grid]):
# #             raise GridException(f"Grid has invalid types: {grid}")
# #         elif any([not str(x).isdigit() for x in grid]):
# #             raise GridException(f"Grid has invalid values: {grid}")
# #         return [int(x) for x in grid]

# #     @classmethod
# #     def _init_values(cls, grid: Any) -> GridArray:
# #         match grid:
# #             case str():
# #                 return cls._parse_str_grid(grid)
# #             case int():
# #                 return cls._parse_int_grid(grid)
# #             case list():
# #                 return cls._parse_list_grid(grid)
# #             case _:
# #                 raise GridException(f"Grid has invalid type: {grid}")

# #     @classmethod
# #     def _init_frozen(cls, values: GridArray) -> GridArray:
# #         return [int(x != cls.MISSING) for x in values]

# #     @classmethod
# #     def _init_dim_sq(cls, values: GridArray) -> int:
# #         if (num_values := len(values)) > cls.MAX_LEN:
# #             raise GridException(f"Grid is too large: {num_values}")
# #         if num_values < cls.MIN_LEN:
# #             raise GridException(f"Grid is too small: {num_values}")
# #         dim_bx: float = math.sqrt(num_values)
# #         dim_sq: float = math.sqrt(int(dim_bx))
# #         if dim_sq != (dim := int(dim_sq)):
# #             raise GridException(f"Grid is non-square: {dim} x `{dim}")
# #         return dim
