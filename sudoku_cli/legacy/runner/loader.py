#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""Sudoku test runner loader."""

import csv
from dataclasses import dataclass
from io import TextIOWrapper

from sudoku_cli.legacy.grid import Grid
from sudoku_cli.runner.results import TestResult
from sudoku_cli.solver import Profiler, Solver


@dataclass
class Test:
    """Test instance with a problem, solution, and identifier.

    Attributes:
        test_id (str): Test identifier string.
        problem (str): Test problem in string format.
        solution (str): Test solution in string format.
    """

    test_id: str
    problem: str
    solution: str


@dataclass
class TestSuite:
    """Test suite with a collection of test instances.

    Attributes:
        tests (list[str]): Collection suite of test instances.
    """

    tests: list[Test]

    def run(self, solver: Solver, params: dict) -> list[Profiler]:
        """Run the test suite on the solver and return each profiler."""
        profiles: list[Profiler] = []
        for test in self.tests:
            grid: Grid = Grid.load_string(test.problem)
            profiles.append(solver.run(grid, **params))
            assert grid.validate() and grid.dump_string() == test.solution
        test_ids: list[str] = [test.test_id for test in self.tests]
        return [TestResult(tid, **pf.__dict__) for tid, pf in zip(test_ids, profiles)]

    @staticmethod
    def load(file: TextIOWrapper, count: int = 1):
        """Load a suite of `count` tests from an opened CSV file."""
        tests: list[Test] = []
        fields: list[str] = ["problem", "solution"]
        for line, obj in enumerate(csv.DictReader(file, fieldnames=fields), start=1):
            if line > count:
                break
            elif line == 1:
                continue
            tests.append(Test(test_id=f"{line:08}", **obj))
        return TestSuite(tests=tests)
