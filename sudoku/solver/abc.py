#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from abc import ABC, abstractmethod

from sudoku.sudoku import Sudoku


class Solver(ABC):
    def __init__(self, sudoku: Sudoku):
        self.sudoku: Sudoku = sudoku

    @abstractmethod
    def setup(self, *args, **kwargs) -> bool:
        raise NotImplementedError

    @abstractmethod
    def solve(self, *args, **kwargs) -> bool:
        raise NotImplementedError

    def check(self, solution: str | None = None) -> bool:
        complete: bool = self.sudoku.is_complete()
        if solution is None:
            return complete
        cells: str = "".join([str(x) for x in self.sudoku.cells.reshape(-1)])
        return complete and cells == solution
