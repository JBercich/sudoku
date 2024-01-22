#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""Experiment runner."""

import argparse
import json
from datetime import datetime
from typing import Final

from sudoku.runner import (
    HyperparameterGrid,
    ParameterResult,
    Result,
    SolverResult,
    TestResult,
    TestSuite,
)
from sudoku.solver import BacktrackingSolver, Profiler, Solver

NUMBER_OF_TESTS: Final[int] = 100
OUTPUT_FILENAME: Final[str] = "test_results.json"

# Define the exhaustive hyperparameter grid
hyperparameter_grid: dict[Solver, dict] = {
    BacktrackingSolver: HyperparameterGrid(
        search_all_values=[True, False],
    )
}

# Build simple argparser to read in test file and test count
parser: argparse.ArgumentParser = argparse.ArgumentParser()
parser.add_argument("filename", type=argparse.FileType("r"))
parser.add_argument("tests", type=int, default=NUMBER_OF_TESTS)

if __name__ == "__main__":
    # Load in args and build the test suite
    args: argparse.Namespace = parser.parse_args()
    suite: TestSuite = TestSuite.load(file=args.filename, count=100)
    timestamp: str = datetime.now().strftime("%Y-%M-%d::%H:%m:%S")
    output_file: str = f"{timestamp}_results.json"
    # Run each solver with each parameter set
    # solver_results: list[SolverResult] = []

    for solver, parameter_list in hyperparameter_grid.items():
        print("Running solver:", solver.__name__)
        # hyperparameter_results: list[ParameterResult] = []
        for parameters in parameter_list:
            print("\tParameters:", parameters)
            profiles: list[Profiler] = suite.run(solver, parameters)
            print(profiles[0])
            # hyperparameter_results.append(TestResult())
            break
    #     solver_results.append(ParameterResult(solver.__name__, hyperparameter_results))
    # result: Result = Result(solvers=solver_results)
