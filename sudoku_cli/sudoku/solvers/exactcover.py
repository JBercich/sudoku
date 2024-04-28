#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from itertools import product
from enum import Enum, unique
from typing import Dict, List, Tuple, TypeAlias, Set

import numpy as np

from sudoku_cli.sudoku import Grid
from sudoku_cli.sudoku.solvers.abc import Solver


@unique
class _Constraint(int, Enum):
    POS = 0
    ROW = 1
    COL = 2
    BOX = 3


ConstraintIdx: TypeAlias = Tuple[int, int]
ConstraintMap: TypeAlias = Tuple[_Constraint, ConstraintIdx]
GridSelection: TypeAlias = Tuple[int, int, int]


class ExactCover(Solver):
    name: str = "ExactCover"

    @classmethod
    def _setup_constraints_and_selections(cls, x_size: int, y_size: int) -> Tuple:
        size: int = x_size * y_size
        constraints: List[ConstraintMap] = (
            [(_Constraint.POS, x) for x in product(range(size), range(size))]
            + [(_Constraint.ROW, x) for x in product(range(size), range(1, size + 1))]
            + [(_Constraint.COL, x) for x in product(range(size), range(1, size + 1))]
            + [(_Constraint.BOX, x) for x in product(range(size), range(1, size + 1))]
        )
        selections: Dict[GridSelection, List[ConstraintMap]] = {}
        for row, col, number in product(range(size), range(size), range(1, size + 1)):
            box: int = (row // x_size) * x_size + (col // y_size)
            selections[(row, col, number)] = [
                (_Constraint.POS, (row, col)),
                (_Constraint.ROW, (row, number)),
                (_Constraint.COL, (col, number)),
                (_Constraint.BOX, (box, number)),
            ]
        return constraints, selections

    @classmethod
    def _setup_constraints_mapping(
        cls,
        constraints: List[ConstraintMap],
        selections: Dict[GridSelection, List[ConstraintMap]],
    ) -> Dict[ConstraintMap, Set[GridSelection]]:
        sets: Dict[ConstraintMap, Set[GridSelection]] = {j: set() for j in constraints}
        for grid_selection, constraint_maps in selections.items():
            for constraint_map in constraint_maps:
                sets[constraint_map].add(grid_selection)
        return sets

    @classmethod
    def solve(cls, grid: Grid, x_size: int = 3, y_size: int = 3):
        print("Setting up exact cover problem.")

        constraints, selections = cls._setup_constraints_and_selections(x_size, y_size)
        constraints_map = cls._setup_constraints_mapping(constraints, selections)

        for (row_idx, col_idx), value in np.ndenumerate(grid.values):
            if value != 0:
                cls.select(constraints_map, selections, (row_idx, col_idx, value))

        for solution in cls.solved(constraints_map, selections, []):
            for r, c, n in solution:
                grid.values[r, c] = n

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
