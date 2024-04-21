#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from abc import ABC, abstractmethod

from sudoku_cli.sudoku import Grid


class Solver(ABC):
    name: str

    @abstractmethod
    @classmethod
    def solve(cls, grid: Grid, *args, **kwargs) -> None:
        pass
