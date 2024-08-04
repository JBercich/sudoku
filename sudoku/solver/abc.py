#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import dataclasses
from abc import ABC, abstractmethod

from sudoku.grid import Grid, Validator


@dataclasses.dataclass(slots=True)
class Solver(ABC):
    grid: Grid
    validator: Validator

    def __post_init__(self) -> None:
        if not self.validator.is_valid(self.grid):
            raise RuntimeError(f"Invalid grid: {self.grid.values}")
        if self.validator.is_complete(self.grid):
            raise RuntimeError("Grid is already complete")

    @abstractmethod
    def solve(self, *args, **kwargs) -> bool:
        raise NotImplementedError
