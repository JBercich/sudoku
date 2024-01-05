#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""Sudoku test runner loader."""

import csv
from dataclasses import dataclass


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

    @staticmethod
    def load(file: str, count: int):
        """Load a suite of `count` tests from a CSV file."""
        tests: list[Test] = []
        fields: list[str] = ["problem", "solution"]
        with open(file, "r") as fp:
            for line, obj in enumerate(csv.DictReader(fp, fieldnames=fields), start=1):
                tests.append(Test(test_id=f"{line:08}", **obj))
                if line >= count:
                    break
        return TestSuite(tests=tests)
