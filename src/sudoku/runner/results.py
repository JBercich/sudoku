#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""Sudoku test results model."""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class TestResult:
    """Single test profile results."""

    test_id: str
    elapsed_time: float
    elapsed_process_time: float
    grid_gets: int
    cell_gets: list[int]
    cell_sets: list[int]


@dataclass
class ParameterResult:
    """Single parameter set profile results."""

    parameters: dict
    tests: list[TestResult]


@dataclass
class SolverResult:
    """Single solver set profile results."""

    name: str
    hyperparameters: list[ParameterResult]


@dataclass
class Result:
    """Full test suite result."""

    solvers: list[SolverResult]
    runtime: datetime = field(default_factory=datetime.now)
