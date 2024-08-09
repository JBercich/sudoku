# #!/usr/bin/env python3
# # -*- coding:utf-8 -*-

# import math
# from typing import Any, TypeAlias

# import numpy as np

# import dataclasses

# CELL_MISSING_VALUE: int = 0
# CELL_MAXIMUM_VALUE: int = 25


# @dataclasses.dataclass(slots=True)
# class Cell:
#     # value: int = CELL_MISSING_VALUE
#     fixed: bool = False
#     getter_cntr: int = 0
#     setter_cntr: int = 0

#     @property
#     def value(self) -> int:
#         self.getter_cntr += 1
#         return self.value

#     @value.setter
#     def value(self, value: Any) -> None:
#         if not isinstance(value, int):
#             raise TypeError(f"cell value must be an integer: {value}")
#         if value <= 0 or value > CELL_MAXIMUM_VALUE:
#             raise ValueError(f"cell value out of bounds [1,25]: {value}")
#         self.setter_cntr += 1
#         self.value = int(value)
