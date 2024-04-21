#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import itertools
import math
from typing import TypeAlias

import numpy as np
import numpy.typing as npt
from typer import BadParameter

DTypeGridValues: TypeAlias = npt.NDArray[np.int8]
DTypeGridFrozen: TypeAlias = npt.NDArray[np.bool_]


class Grid:
    def __init__(self, grid: str):
        dim: float = math.sqrt(len(grid))
        self.dim: int = int(dim)
        if self.dim != dim:
            raise BadParameter(f"Grid size must be square, not length {len(grid)}.")
        self.values: DTypeGridValues = np.array(list(grid), dtype=np.int8)
        self.values = self.values.reshape((self.dim, self.dim))
        self.frozen: DTypeGridFrozen = np.copy(self.values) != 0

    def is_complete(self) -> bool:
        iter_range: range = range(0, self.dim, self.dim // 3)
        for row in self.values:
            if 0 in row or any([v > 1 for v in np.unique(row, return_counts=True)[1]]):
                return False
        for col in self.values.T:
            if 0 in col or any([v > 1 for v in np.unique(col, return_counts=True)[1]]):
                return False
        for row, col in itertools.product(iter_range, iter_range):
            row_to: int = row + self.dim // 3
            col_to: int = col + self.dim // 3
            sub: DTypeGridValues = self.values[row:row_to, col:col_to]
            if 0 in sub or any([v > 1 for v in np.unique(sub, return_counts=True)[1]]):
                return False
        return True
