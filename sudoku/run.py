#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""Experiment runner."""

import csv
import json
from dataclasses import asdict
from itertools import product

from sudoku.grid import Grid
from sudoku.solver import BacktrackingSolver, Profiler, Solver


class HyperparameterGrid:
    """Hyperparameter grid constructor."""

    @staticmethod
    def __new__(self, **kwargs) -> dict:
        # Check all hyperparameter options are given as lists
        for k, v in kwargs.items():
            if not isinstance(v, list):
                raise ValueError(f"Hyperparameter grid requires list of options: {k}")
        # Create cartesian product of hyperparameters
        return [
            {parameter: value for parameter, value in zip(kwargs.keys(), parameter_set)}
            for parameter_set in [
                parameter_subset for parameter_subset in product(*kwargs.values())
            ]
        ]


HYPERPARAMETER_GRID: dict[Solver, dict] = {
    BacktrackingSolver: HyperparameterGrid(
        search_all_values=[True, False],
    )
}

SUDOKU_TEST_FILE: str = "data/sudoku.csv"
SUDOKU_TEST_COUNT: int = 100
SUDOKU_TEST_OUTPUT: str = "output.json"

if __name__ == "__main__":
    # Collect testing examples
    examples: list[tuple] = []
    with open(SUDOKU_TEST_FILE, "r") as example_file:
        for i, (problem, solution) in enumerate(csv.reader(example_file), 0):
            if i <= 100:
                continue
            examples.append((problem, solution))
            if i >= 100 + SUDOKU_TEST_COUNT:
                break
    # Run the tests
    for solver, hparams in HYPERPARAMETER_GRID.items():
        print("Solver:", solver.__name__)
        for hparam in hparams:
            print("Parameters:", hparam)
            for problem, solution in examples:
                problem: Grid = Grid.load_string(problem)
                # profiler: Profiler = solver.run(problem, **hparam)
                # assert problem.validate()
    # print(asdict(profiler))
