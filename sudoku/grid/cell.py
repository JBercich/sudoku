#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""Cell abstraction."""

from __future__ import annotations

import warnings
from dataclasses import dataclass, field
from typing import Any, Final, Iterable

EMPTY_CELL_VALUE: Final[int] = 0
DEFAULT_CELL_MINIMUM: Final[int] = 1
DEFAULT_CELL_MAXIMUM: Final[int] = 9


from pydantic import BaseModel, Field


class Cell(BaseModel):
    value: int = Field(..., description="")
    maximum_value: int = Field(..., description="")


#     value: int = field(default=EMPTY_CELL_VALUE, repr=T`rue)
#     static: bool = field(default=False, repr=True)
#     maximum_value: bool = field(default=DEFAULT_CELL_MAXIMUM, repr=True)
#     minimum_value: bool = field(default=DEFAULT_CELL_MINIMUM, repr=False)
#     _getter_counter: int = field(default=0, repr=True)
#     _setter_counter: int = field(default=0, repr=True)

#     # value
#     # -----
#     # Overloading of the `value` field is done to constrain attribute setting and also
#     # profile cell time complexity by instance gets and sets. NOTE: a static cell cannot
#     # be modified and will raise a RuntimeError.

#     @property
#     def value(self) -> int:
#         pass

#     @value.setter
#     def value(self, value: Any) -> None:
#         if isinstance(value, property):
#             value: int = EMPTY_CELL_VALUE
#         if not self.value_is_valid(value):
#             raise ValueError(f"Invalid cell value: {value}")
#         if self.static:
#             raise RuntimeError("Cannot modify a static cell.")
#         self._setter_counter += 1
#         self._value: int = value

#     @value.getter
#     def value(self) -> int:
#         self._getter_counter += 1
#         return self._value

#     # minimum_value
#     # -------------
#     # Cell minimum value is an accessible field with a valid getter, but the setter is
#     # overloaded to prevent skewed bounds for the cell range. The lower bound minimum is
#     # kept as `DEFAULT_CELL_MINIMUM`. It cannot be set during initialisation also.

#     @property
#     def minimum_value(self) -> int:
#         pass

#     @minimum_value.setter
#     def minimum_value(self, minimum_value: int) -> None:
#         if not isinstance(minimum_value, property):
#             warnings.warn(f"Unable to set minimum value of a cell: {minimum_value}")
#         return

#     @minimum_value.getter
#     def minimum_value(self) -> int:
#         return DEFAULT_CELL_MINIMUM

#     # Dunder methods
#     # --------------
#     # Builtin dunders are overloaded to make cells easier to use in more complex logic
#     # associated with the grid and solvers. It will allow further collection logic in a
#     # wrapper grid as well as additional operations.

#     def __eq__(self, other: Cell) -> bool:
#         """Instance equality method by value."""
#         return self.value == other.value

#     def __lt__(self, other: Cell) -> bool:
#         """Instance less than method by value."""
#         return self.value < other.value

#     def __str__(self) -> str:
#         """Instance string method for value stdout."""
#         return str(self.value)

#     def __hash__(self) -> int:
#         """Instance hash method for value."""
#         return hash(self.value)

#     # Helper methods
#     # --------------
#     # Additional methods are made to extend the readability of internal cell logic.
#     # Simple logic shortcuts made to reduce overhead when constructing larger and more
#     # dense code chunks helps improve algorithm design and enhancement to modular parts.

#     def set_empty_value(self) -> None:
#         """Set the cell value to the empty encoding."""
#         self.value = EMPTY_CELL_VALUE

#     def is_empty(self) -> bool:
#         """Cell is empty with the value encoded as empty."""
#         return self.value == EMPTY_CELL_VALUE

#     def value_is_valid(self, value: int) -> bool:
#         """Value is in the valid range for the cell (including empty encoding)."""
#         valid_value_range: Iterable = range(self.maximum_value + 1)
#         return value in valid_value_range

#     # Counter methods
#     # ---------------
#     # Certain cell-wrapping methods may further modify cells which can inadvertedly set
#     # or get the value field modifying the cell counters. Reset functions are used to
#     # allow more precise cell usage.

#     def reset_getter_counter(self):
#         """Reset the getter counter to 0."""
#         self._getter_counter = 0

#     def reset_setter_counter(self):
#         """Reset the setter counter to 0."""
#         self._setter_counter = 0

#     def reset_counters(self):
#         """Reset the getter and setter counters to 0."""
#         self.reset_getter_counter()
#         self.reset_setter_counter()
