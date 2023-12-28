#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import csv
import warnings
from pathlib import Path

import pytest

EXAMPLE_TEST_FILE: Path = Path(__file__).parent / "examples.csv"


@pytest.fixture(scope="session")
def sudoku_tests():
    """Yield a list of tuple pairs of problems and solutions for test examples."""

    # Load in the csv file example pairs
    examples: list[tuple] = []
    with open(EXAMPLE_TEST_FILE, "r") as example_file:
        for problem, solution in csv.reader(example_file):
            examples.append((problem, solution))
    return examples


@pytest.fixture(scope="function")
def filter_cell_warnings():
    """Ignore cell warnings when overriding the minimum_value field."""
    warnings.simplefilter("ignore")
