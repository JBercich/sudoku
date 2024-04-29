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
    def _reduce_constraints(
        cls,
        constraints_map: Dict[ConstraintMap, Set[GridSelection]],
        selections: Dict[GridSelection, List[ConstraintMap]],
        index: GridSelection,
    ) -> List[Set[GridSelection]]:
        selected_contraints: List[Set[GridSelection]] = []
        for constraint in selections[index]:
            for selection in constraints_map[constraint]:
                for selection_constraint in selections[selection]:
                    if selection_constraint != constraint:
                        constraints_map[selection_constraint].remove(selection)
            selected_contraints.append(constraints_map.pop(constraint))
        return selected_contraints

    @classmethod
    def _restore_constraints(
        cls,
        constraints_map: Dict[ConstraintMap, Set[GridSelection]],
        selections: Dict[GridSelection, List[ConstraintMap]],
        index: GridSelection,
        selected_contraints: List[Set[GridSelection]],
    ) -> None:
        for constraints in reversed(selections[index]):
            constraints_map[constraints] = selected_contraints.pop()
            for selection in constraints_map[constraints]:
                for selection_iter in selections[selection]:
                    if selection_iter != constraints:
                        constraints_map[selection_iter].add(selection)

    @classmethod
    def _generate_solutions(
        cls,
        constraints_map: Dict[ConstraintMap, Set[GridSelection]],
        selections: Dict[GridSelection, List[ConstraintMap]],
        grids: List[GridSelection] = [],
    ):
        if not constraints_map:
            yield list(grids)
        else:
            constraint = min(constraints_map, key=lambda c: len(constraints_map[c]))
            for index in list(constraints_map[constraint]):
                grids.append(index)
                subsets = cls._reduce_constraints(constraints_map, selections, index)
                for grid in cls._generate_solutions(constraints_map, selections, grids):
                    yield grid
                cls._restore_constraints(constraints_map, selections, index, subsets)
                grids.pop()

    @classmethod
    def solve(cls, grid: Grid, x_size: int = 3, y_size: int = 3):
        constraints, selections = cls._setup_constraints_and_selections(x_size, y_size)
        constraints_map = cls._setup_constraints_mapping(constraints, selections)

        for (row, col), value in np.ndenumerate(grid.values):
            if value != 0:
                cls._reduce_constraints(constraints_map, selections, (row, col, value))

        for solution_index in cls._generate_solutions(constraints_map, selections, []):
            for row, col, value in solution_index:
                grid.values[row, col] = value
            break
