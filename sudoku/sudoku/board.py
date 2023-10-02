#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import re


class SudokuBoard:
    """
    Sudoku board.

    A sudoku board can be solved by a solver. The default and most portable format for
    the boards is a single string of cells from left-right and top-down. A 0 encodes the
    empty cell for an incomplete board.
    """

    SIZE: int = 3
    MISS: str = "0"
    WIDTH: int = 9
    CELLS: int = 81

    def __init__(self, board: str) -> None:
        self.board: str = self.validate(board)

    def validate(self, board: str, complete: bool = False) -> str:
        """
        Validate the input string-format board.

        For the default input format of a string board, validation of the input is done
        to confirm whether the board is valid from an initial level. Only constraints
        are checked such as column, row and grid restrictions.
        """
        # Check the correctness of the input board string
        if not isinstance(board, str):
            raise ValueError(f"board must be {str}, not {type(board)}")

        # Verify that the board has the valid characters
        if re.fullmatch(r"[0-9].{80}", board) is None:
            raise ValueError("board must have 81 cells with digits 0-9")

        # Check whether the board needs to be completed
        if self.MISS in board and complete:
            raise ValueError("board must be complete but has missing field")

        # Check that the different sudoku board fields are held for all board segments
        for i in range(self.WIDTH):
            # Get lists of each of the constrained sudoku board fields
            row: list = [board[i + p] for p in range(0, self.WIDTH)]
            col: list = [board[i + p] for p in range(0, self.CELLS, self.WIDTH)]
            grid: list = [
                board[(i * self.SIZE) + (r * self.WIDTH) + c]
                for r in range(self.SIZE)
                for c in range(self.SIZE)
            ]
            # Check if the board is complete
            for field in [row, col, grid]:
                for j in range(1, self.WIDTH + 1):
                    if field.count(j) > 1:
                        raise ValueError(f"invalid row, column or grid: {field}")

        return board

    def __getitem__(self, index):
        return self.board[index]
