#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""Cell abstraction."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Final

DEFAULT_CELL_MINIMUM: Final[int] = 1
DEFAULT_CELL_MAXIMUM: Final[int] = 9


@dataclass(slots=True)
class Cell:
    """Sudoku grid cell.

    Grid cells contain a value and must uphold sudoku constraints. This implementation
    has full customisability over cell constraints to simplify usage of the cell in a
    grid setting with different configurations. Only numbers will be used to encode the
    values of a cell with 0 required as empty and n-m for some bounded range [n,m].

    Attributes:
        value (int, optional): Integer value contained in the cell. Ranges in value from
            n-m or encoded as empty. Defaults to `EMPTY_VALUE`.
        static (bool, optional): Cell is frozen and the value cannot be modified.
            Defaults to False.
        minimum_value (int, optional): Minimum allowed value for the cell to be set to.
            Defaults to `DEFAULT_CELL_MINIMUM`.
        maximum_value (int, optional): Maximum allowed value for the cell to be set to.
            Defaults to `DEFAULT_CELL_MAXIMUM`.
    """

    EMPTY_VALUE: Final[int] = 0

    value: int = field(default=EMPTY_VALUE)
    static: bool = field(default=False, repr=False)
    minimum_value: bool = field(default=DEFAULT_CELL_MINIMUM, repr=False)
    maximum_value: bool = field(default=DEFAULT_CELL_MAXIMUM, repr=False)
    _getter_counter: int = field(default=0, repr=False)
    _setter_counter: int = field(default=0, repr=False)

    @property
    def value(self) -> int:
        """Value property getter."""

        # Update the getter counter and return the value
        self._getter_counter += 1
        return self._value

    @value.setter
    def value(self, value: int):
        """Value property setter."""

        # Cells cannot be modified if they are static
        if self.static:
            raise RuntimeError("Cannot modified a static cell.")

        # Cells cannot be modified with an invalid value outside of the accepted range
        if value not in range(self.minimum_value, self.maximum_value + 1):
            raise ValueError(f"Invalid cell value: {value}")

        # Update the setter counter and set the value
        self._setter_counter += 1
        self._value: int = value

    def __eq__(self, other: Cell) -> bool:
        """Instance equality method by value."""
        return self.value == other.value

    def __lt__(self, other: Cell) -> bool:
        """Instance less than method by value."""
        return self.value < other.value

    def __str__(self) -> str:
        """Instance string method for value stdout."""
        return str(self.value)

    def __repr__(self) -> str:
        """Instance repr. method for value stdout."""
        return self.__str__()

    def reset_getter_counter(self):
        """Reset the getter counter to 0."""
        self._getter_counter = 0

    def reset_setter_counter(self):
        """Reset the setter counter to 0."""
        self._setter_counter = 0

    def reset_counters(self):
        """Reset the getter and setter counters to 0."""
        self.reset_getter_counter()
        self.reset_setter_counter()
