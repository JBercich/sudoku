#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from sudoku.sudoku.board.board import SudokuBoard


class SudokuBoardV1(SudokuBoard):
    """
    Data Type: `list[int]`

    Builtin Python integer list representation of a board. A standard and simple way to
    create the board that can be done with minimal effort. Requires a single value index
    to access the list in the same board representation as the input string board.
    """

    NAME: str = "V1: Python List"
    DESC: str = "Simple implementation of a Python builtin list of integers"

    def setup(self, board: str) -> list[int]:
        return [int(v) for v in board]

    def to_string(self) -> str:
        return "".join([str(v) for v in self.board])
