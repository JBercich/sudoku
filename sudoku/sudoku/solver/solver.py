#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from abc import ABC, abstractclassmethod

from sudoku.sudoku.board import SudokuBoard


class SudokuSolver(ABC):
    """
    Sudoku solver abstraction.

    Solver algorithms are run from the solver class. This allows for convenient modular
    portability of solving algorithms with the different appropriate boards. Each class
    only needs to implement the `solve()` algorithm to be usable.
    """

    @abstractclassmethod
    def solve(cls, board: SudokuBoard) -> SudokuBoard:
        """
        Solver function.

        Given a board, this function solves a sudoku board and returns the completed
        board in its suitable format. External board functionality is used to convert
        between different board formats.
        """
        pass
