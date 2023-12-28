#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import pytest

from sudoku.grid import Grid
from sudoku.solver import Solver, BacktrackingSolver

TESTABLE_SOLVERS: list[Solver] = [
    BacktrackingSolver,
]


class TestSolvers:
    @pytest.mark.parametrize("solver", TESTABLE_SOLVERS)
    def test_solver_correctness(self, sudoku_tests: list[tuple], solver: Solver):
        """Run each solver with the example test files to ensure overall correctness."""

        # Iterate through each test for the solver
        for problem, solution in sudoku_tests:
            grid: Grid = Grid.load_string(problem)
            grid, _ = solver.solve(grid)
            assert grid.dump_string() == solution
