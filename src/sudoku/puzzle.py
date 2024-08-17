# #!/usr/bin/env python3
# # -*- coding:utf-8 -*-

# import math
# from typing import Any, TypeAlias
# from enum import Enum, unique

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


# print(_generate_box_idxs(3))


# # print(list(itertools.repeat(list(range(puzzle_size)), 2)))


# # PuzzleArray: TypeAlias = list[int] | np.ndarray


# # @unique
# # class _SizeMapping(Enum, tuple[int, int, int]):


# # class Puzzle:
# #     MISSING: int = 0
# #     MIN_DIM: int = 1
# #     MIN_LEN: int = 1
# #     MAX_DIM: int = 5
# #     MAX_LEN: int = 625

# #     def __init__(self, puzzle: Any):
# #         self.values: GridArray = self._init_values(grid)
# #         self.frozen: GridArray = self._init_frozen(self.values)
# #         self.dim_sq: int = self._init_dim_sq(self.values)
# #         self.dim_bx: int = int(self.dim_sq**2)

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
