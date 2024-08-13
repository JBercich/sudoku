#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import numpy as np


class Sudoku:
    def __init__(self, *, cells: str):
        self.cells: np.ndarray = self._cells_str_to_array(cells)
        self.cells_frozen: np.ndarray = np.copy(self.cells)
        self.grid_size: int = int(np.sqrt(self.cells.size))
        self.box_size: int = int(np.sqrt(self.grid_size))
        self.shape: tuple[int, int] = (self.grid_size, self.grid_size)

    @classmethod
    def _cells_str_to_array(cls, cells: str) -> np.ndarray:
        tmp_cells: list[int] = [int(x) for x in cells]
        dim: int = int(np.sqrt(len(tmp_cells)))
        return np.asarray(tmp_cells, dtype=np.uint8).reshape((dim, dim))

    def __str__(self) -> str:
        return self.cells.__str__()

    def __repr__(self) -> str:
        return self.cells.__repr__()

    def get_row_by_idx(self, row: int) -> np.ndarray:
        return self.cells[row, :]

    def get_col_by_idx(self, col: int) -> np.ndarray:
        return self.cells[:, col]

    def get_box_by_idx(self, row: int, col: int) -> np.ndarray:
        i: int = (row // self.box_size) * self.box_size
        j: int = (col // self.box_size) * self.box_size
        return self.cells[i : i + self.box_size, j : j + self.box_size]

    def get_box_by_num(self, box: int) -> np.ndarray:
        row: int = box // self.box_size * self.box_size
        col: int = box % self.box_size * self.box_size
        return self.cells[row : row + self.box_size, col : col + self.box_size]

    def validate_row_by_idx(self, row: int) -> bool:
        arr: np.ndarray = self.get_row_by_idx(row)
        return np.unique(arr[arr != 0]).size == arr[arr != 0].size

    def validate_col_by_idx(self, col: int) -> bool:
        arr: np.ndarray = self.get_col_by_idx(col)
        return np.unique(arr[arr != 0]).size == arr[arr != 0].size

    def validate_box_by_idx(self, row: int, col: int) -> bool:
        arr: np.ndarray = self.get_box_by_idx(row, col)
        return np.unique(arr[arr != 0]).size == arr[arr != 0].size

    def validate_box_by_num(self, box: int) -> bool:
        arr: np.ndarray = self.get_box_by_num(box)
        return np.unique(arr[arr != 0]).size == arr[arr != 0].size

    def cell_is_valid(self, i: int, j: int) -> bool:
        if not self.validate_row_by_idx(i):
            return False
        if not self.validate_col_by_idx(j):
            return False
        if not self.validate_box_by_idx(i, j):
            return False
        return True

    def is_valid(self) -> bool:
        for i in range(self.grid_size):
            if not self.validate_row_by_idx(i):
                return False
            if not self.validate_col_by_idx(i):
                return False
            if not self.validate_box_by_num(i):
                return False
        return True

    def is_complete(self) -> bool:
        return self.is_valid() and np.sum(self.cells == 0) == 0
