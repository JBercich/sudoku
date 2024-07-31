# #!/usr/bin/env python3
# # -*- coding:utf-8 -*-

# import itertools
# import math
# from typing import TypeAlias

# import numpy as np
# import numpy.typing as npt

# from typer import BadParameter

# DTypeGridValues: TypeAlias = npt.NDArray[np.int8]
# DTypeGridFrozen: TypeAlias = npt.NDArray[np.bool_]


# class Grid:
#     def __init__(self, grid: str):
#         dim: float = math.sqrt(len(grid))
#         self.dim: int = int(dim)
#         if self.dim != dim:
#             raise BadParameter(f"Grid size must be square, not length {len(grid)}.")
#         self.values: DTypeGridValues = np.array(list(grid), dtype=np.int8)
#         self.values = self.values.reshape((self.dim, self.dim))
#         self.frozen: DTypeGridFrozen = np.copy(self.values) != 0

#     def check_row_constraint(self, row_idx: int) -> bool:
#         assert row_idx in range(9)
#         vals, counts = np.unique(self.values[row_idx, :], return_counts=True)
#         if any([v > 1 for k, v in zip(vals, counts) if k != 0]):
#             return False
#         return True

#     def check_col_constraint(self, col_idx: int) -> bool:
#         assert col_idx in range(9)
#         vals, counts = np.unique(self.values[:, col_idx], return_counts=True)
#         if any([v > 1 for k, v in zip(vals, counts) if k != 0]):
#             return False
#         return True

#     def check_subgrid_constraint(self, row_idx: int, col_idx: int) -> bool:
#         assert row_idx in range(9) and col_idx in range(9)
#         row_idx = row_idx - (row_idx % 3)
#         col_idx = col_idx - (col_idx % 3)
#         sub: DTypeGridValues = self.values[row_idx : row_idx + 3, col_idx : col_idx + 3]
#         vals, counts = np.unique(sub, return_counts=True)
#         if any([v > 1 for k, v in zip(vals, counts) if k != 0]):
#             return False
#         return True

#     def is_valid(self) -> bool:
#         for idx in range(9):
#             if self.check_row_constraint(idx) and self.check_col_constraint(idx):
#                 continue
#             return False
#         for row_idx, col_idx in itertools.product(range(9, 3), range(9, 3)):
#             if self.check_subgrid_constraint(row_idx, col_idx):
#                 continue
#             return False
#         return True

#     def is_complete(self) -> bool:
#         return self.is_valid() and 0 not in self.values
