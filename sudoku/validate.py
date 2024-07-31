# #!/usr/bin/env python3
# # -*- coding:utf-8 -*-

# from abc import ABC, abstractmethod
# from typing import Iterable

# class GridValidator(ABC):
#     @classmethod
#     @abstractmethod
#     def validate(cls, grid):
#         raise NotImplementedError

#     @staticmethod
#     def check_constraint(values: Iterable):
#         subset: set = set(values)
#         subset_is_incomplete: bool = 0 in subset
#         if 0 not in subset and len(subset) == len(values):
#             return True
#         elif 0 in subset

#         return False


# class FullGridValidator(GridValidator):
#     @classmethod
#     def validate(cls, grid):
#         print(grid)
#         if not cls.check_constraint(grid[:9]):
#             raise Exception


# x = [int(i) for i in "002085700000607000000100000400001007267504000001000090518700430030010506900003001"]

# FullGridValidator.validate(x)


# # def check_row_constraint(self, row_idx: int) -> bool:
# #     assert row_idx in range(9)
# #     vals, counts = np.unique(self.values[row_idx, :], return_counts=True)
# #     if any([v > 1 for k, v in zip(vals, counts) if k != 0]):
# #         return False
# #     return True

# # def check_col_constraint(self, col_idx: int) -> bool:
# #     assert col_idx in range(9)
# #     vals, counts = np.unique(self.values[:, col_idx], return_counts=True)
# #     if any([v > 1 for k, v in zip(vals, counts) if k != 0]):
# #         return False
# #     return True

# # def check_subgrid_constraint(self, row_idx: int, col_idx: int) -> bool:
# #     assert row_idx in range(9) and col_idx in range(9)
# #     row_idx = row_idx - (row_idx % 3)
# #     col_idx = col_idx - (col_idx % 3)
# #     sub: DTypeGridValues = self.values[row_idx : row_idx + 3, col_idx : col_idx + 3]
# #     vals, counts = np.unique(sub, return_counts=True)
# #     if any([v > 1 for k, v in zip(vals, counts) if k != 0]):
# #         return False
# #     return True
