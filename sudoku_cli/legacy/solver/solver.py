#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""Solver abstraction."""

from abc import ABC, abstractclassmethod
from typing import Any

from sudoku_cli.legacy.grid import Grid
from sudoku_cli.solver.profiler import Profiler


class Solver(ABC):
    """Base abstract solver.

    Single function wrapper for running a solver method. Each solver extends the method
    used to solve an input grid with aset of parameters. The runtime solver is profiled
    to extract certain metrics of the algorithm to better showcase how certain methods
    solve the sudoku board.
    """

    @classmethod
    def run(cls, grid: Grid, **params) -> None:
        """Main solver entrypoint function for a sudoku grid solver."""
        profiler: Profiler = Profiler(grid=grid)
        profiler.start()
        cls.solve(grid, **params)
        profiler.stop()
        return profiler

    @abstractclassmethod
    def solve(cls, grid: Grid, **params) -> Any:
        """Abstract method for solving a grid in different solvers."""
        pass
