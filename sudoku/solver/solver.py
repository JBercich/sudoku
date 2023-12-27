#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""Base solver abstract class."""

import time
from abc import ABC, abstractclassmethod

from sudoku.grid import Grid


class Solver(ABC):
    """Base solver abstract class."""

    @classmethod
    def solve(cls, grid: Grid, **solver_params) -> Grid:
        """Generic solve function for sudoku grids."""

        # Perform generic solve, add time profiling
        start_process_time: float = time.process_time()
        cls._solve(grid, **solver_params)
        end_process_time: float = time.process_time()
        elapsed_process_time: float = end_process_time - start_process_time
        return grid, elapsed_process_time

    @abstractclassmethod
    def _solve(cls, grid: Grid, **params) -> Grid:
        """Abstract method to overload for solving a grid in child class solvers."""

        return grid
