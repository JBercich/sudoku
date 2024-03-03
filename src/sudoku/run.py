#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import argparse
import csv
import dataclasses
import datetime
import re

# Argparser for reading in a sudoku test file CSV with comma-delimited 'test,solution'
parser: argparse.ArgumentParser = argparse.ArgumentParser()
parser.add_argument("--num_tests", "-n", type=int, default=1000)
parser.add_argument("--input_pth", "-i", type=argparse.FileType("r"), required=True)


# Populate a simple test suite
@dataclasses.dataclass
class Test:
    test_no: int
    problem: str
    solution: str

    def __post_init__(self):
        # Regex matching the expected sudoku problem without rule validation
        if re.match(r"^[0-9]{81}$", self.problem) is None:
            raise RuntimeError(f"Invalid sudoku problem: {self.problem}")
        if re.match(r"^[1-9]{81}$", self.solution) is None:
            raise RuntimeError(f"Invalid sudoku solution: {self.solution}")


if __name__ == "__main__":
    # Load in args and build the test suite
    args: argparse.Namespace = parser.parse_args()
    timestamp: str = datetime.datetime.now().strftime("%Y-%M-%dT%H:%m:%S")
    output_filename: str = f"{timestamp}-sudoku-results-{args.num_tests}.csv"

    # Setup the test collection and loop, perform simple validation on input fields
    count: int = 1
    tests: list[Test] = []
    for row in csv.DictReader(args.input_pth, ["problem", "solution"]):
        tests.append(Test(count, row["problem"], row["solution"]))
        if count >= args.num_tests:
            break
        count += 1

    # Run each test
    for test in tests:
        print(f"{test.test_no:>5d} {test.problem}")
