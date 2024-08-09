#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import pathlib

import pytest

test_file: pathlib.Path = pathlib.Path(__file__).parent / "tests.csv"


@pytest.fixture
def grids() -> list[tuple[str, str]]:
    test_grids: list[tuple[str, str]] = []
    with open(test_file, "r") as fp:
        for line in fp:
            problem, solution = line.strip().split(",")
            test_grids.append((problem, solution))
    return test_grids
