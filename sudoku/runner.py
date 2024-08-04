#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import timeit

import numpy as np

from sudoku.grid import Grid, NumpyGrid, Validator
from sudoku.solver.backtracking import BackTrackingSolver

with open(file="examples.csv", mode="r") as fp:
    problems = fp.readlines()


print(timeit.timeit(lambda: [Grid(x) for x in problems], number=10) / 10)
print(timeit.timeit(lambda: [NumpyGrid(x) for x in problems], number=10) / 10)


grids = [Grid(x) for x in problems]
times = []
for grid in grids:
    timer = timeit.timeit(BackTrackingSolver(grid, Validator()).solve, number=1)
    times.append(timer)
    print("->", timer)
    assert Validator.is_complete(grid)


print(np.mean(times))


# np grid 0.055576623379984084
# normal 0.03525952410993341
