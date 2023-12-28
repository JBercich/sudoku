#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""Sudoku cell dataclass."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Cell:
    """Sudoku board cell."""

    _MIN: int = 0
    _MAX: int = 9

    value: int
    static: bool = False
    _get_count: int = field(default=0, repr=False)
    _set_count: int = field(default=0, repr=False)

    @property
    def value(self) -> int:
        """Value property for overriding dataclass setter/getter."""
        return self._value

    @value.setter
    def value(self, value: int):
        """Custom value setter for upholding value constraints (le=9,ge=0)."""
        if value < self._MIN or value > self._MAX:
            raise ValueError(f"Invalid cell value: {value}")
        if self.static:
            return
        self._set_count += 1
        self._value: int = value

    @value.getter
    def value(self) -> int:
        """Custom value getter for incrementing field access counter."""
        self._get_count += 1
        return self._value

    def __eq__(self, other: Cell) -> bool:
        """Custom equality dunder method for comparing instances."""
        return self.value == other.value

    def __lt__(self, other: Cell) -> bool:
        """Custom less than dunder method for comparing instances in collection sort."""
        return self.value < other.value

    def __str__(self) -> str:
        """Custom string dunder method for stdout."""
        return str(self.value)

    def __repr__(self) -> str:
        """Custom representation dunder method for stdout."""
        return self.__str__()

    def reset_counters(self):
        """Reset the getter and setter counters to 0."""
        self._get_count = 0
        self._set_count = 0
