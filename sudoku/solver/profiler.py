#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""Profiler abstraction."""

import time
from dataclasses import dataclass, field
from typing import Optional

from sudoku.grid import Grid


@dataclass
class Profiler:
    """Solver profiler.

    Simple container class for storing sudok solver profiles for when running a solver
    algorithm. This is used with a simple instance `start` and `stop` method pair to run
    immediately before and after a solver algorithm.

    Attributes:
        grid (Grid):
        elapsed_time (float, optional): Elapsed time for the solver. Defaults to None.
        elapsed_process_time (float, optional): Elapsed process thread time of the
            solver. Defaults to None.
        grid_gets (int, optional): Grid getter counter. Defaults to None.
        cell_gets (list[int], optional): Cell getter counter. Defaults to None.
        cell_sets (list[int], optional): Cell setter counter. Defaults to None.
    """

    grid: Grid = field(repr=False)
    elapsed_time: Optional[float] = field(default=None, repr=True)
    elapsed_process_time: Optional[float] = field(default=None, repr=True)
    grid_gets: Optional[int] = field(default=None, repr=False)
    cell_gets: Optional[list[int]] = field(default=None, repr=False)
    cell_sets: Optional[list[int]] = field(default=None, repr=False)

    _start_time: int = field(default=0, repr=False)
    _stop_time: int = field(default=0, repr=False)
    _start_process_time: int = field(default=0, repr=False)
    _stop_process_time: int = field(default=0, repr=False)

    def start(self):
        """Starts the profiler metrics to start tracking resources."""
        self._start_time = time.time()
        self._start_process_time = time.process_time()

    def stop(self):
        """Stops the profiler metrics from running."""
        self._stop_time = time.time()
        self._stop_process_time = time.process_time()
        self.elapsed_time = self._stop_time - self._start_time
        self.elapsed_process_time = self._stop_process_time - self._start_process_time
        self.grid_gets = self.grid._getter_counter
        self.cell_gets = [cell._getter_counter for cell in self.grid]
        self.cell_sets = [cell._setter_counter for cell in self.grid]
