#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from itertools import product

from sudoku_cli.sudoku import Grid
from sudoku_cli.sudoku.solvers.abc import Solver


class ExactCover(Solver):
    name: str = "ExactCover"

    # @classmethod
    # def _setup_constraints(cls) -> Dict:

    @classmethod
    def solve(cls, grid: Grid):
        print("Setting up exact cover problem.")

        R, C = (3, 3)
        N = R * C
        X = (
            [("rc", rc) for rc in product(range(N), range(N))]
            + [("rn", rn) for rn in product(range(N), range(1, N + 1))]
            + [("cn", cn) for cn in product(range(N), range(1, N + 1))]
            + [("bn", bn) for bn in product(range(N), range(1, N + 1))]
        )

        print(len(X) / 4, X[:5])

        Y = dict()

        for r, c, n in product(range(N), range(N), range(1, N + 1)):
            b = (r // R) * R + (c // C)  # Box number
            Y[(r, c, n)] = [
                ("rc", (r, c)),
                ("rn", (r, n)),
                ("cn", (c, n)),
                ("bn", (b, n)),
            ]

        print(list(Y.keys())[0])
        X, Y = cls.exact_cover(X, Y)
        print(len(list(Y.keys())), len(X))
        # print(Y)

        # print(len(X))
        for i, row in enumerate(grid.values):
            for j, n in enumerate(row):
                if n:
                    cls.select(X, Y, (i, j, n))
        # print(len(X))

        for solution in cls.solved(X, Y, []):
            for r, c, n in solution:
                grid.values[r, c] = n

    @classmethod
    def exact_cover(cls, X, Y):
        X = {j: set() for j in X}
        for i, row in Y.items():
            print(i, row)
            for j in row:
                X[j].add(i)
        return X, Y

    @classmethod
    def solved(cls, X, Y, solution):
        if not X:
            yield list(solution)
        else:
            c = min(X, key=lambda c: len(X[c]))
            for r in list(X[c]):
                solution.append(r)
                cols = cls.select(X, Y, r)
                for s in cls.solved(X, Y, solution):
                    yield s
                cls.deselect(X, Y, r, cols)
                solution.pop()

    @classmethod
    def select(cls, X, Y, r):
        cols = []
        for j in Y[r]:
            for i in X[j]:
                for k in Y[i]:
                    if k != j:
                        X[k].remove(i)
            cols.append(X.pop(j))
        return cols

    @classmethod
    def deselect(cls, X, Y, r, cols):
        for j in reversed(Y[r]):
            X[j] = cols.pop()
            for i in X[j]:
                for k in Y[i]:
                    if k != j:
                        X[k].add(i)
