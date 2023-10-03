#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import time
from copy import deepcopy


from sudoku.sudoku.board.board import SudokuBoard
from sudoku.sudoku.solver.solver import SudokuSolver


class SudokuSolverV1(SudokuSolver):
    @staticmethod
    def board_is_valid(board: list[int], complete: bool = False) -> bool:
        """
        TODO
        """

        for i in range(9):
            row: list = [board[(i * 9) + p] for p in range(0, 9)]
            col: list = [board[i + p] for p in range(0, 81, 9)]
            grid: list = [
                board[((i % 3) * 3 + (i // 3) * 27) + (r * 9) + c]
                for r in range(3)
                for c in range(3)
            ]
            for k, field in enumerate([row, col, grid]):
                for j in range(1, 9 + 1):
                    if field.count(j) > 1:
                        if complete and field.count(0) > 0:
                            return False
                        return False
        return True

    @staticmethod
    def recursive_solve(
        index: int,
        board: list[int],
        static_indexes: list[int],
    ) -> list[int]:
        """
        TODO
        """

        # Obtain metrics for this run
        start_time: int = time.time()
        increments: int = 0

        # Terminal case: All cells complete
        if index == 81:
            return board

        # Skip case: Index is a static cell
        if index in static_indexes:
            return SudokuSolverV1.recursive_solve(index + 1, board, static_indexes)

        # Recursive case: Update the cell and any previous cells until valid
        board[index] = 1
        board_limit: list[int] = deepcopy(board)
        while not SudokuSolverV1.board_is_valid(board, False if index != 80 else True):
            # Print updating information for the running cell
            ups: int = int(increments / (time.time() - start_time))
            print(f"Cell Update: {index} ({increments}) - {ups}ps", end="\r")
            if increments % 100000 == 0:
                print("".join([str(i) for i in board]))

            # Iterate backwards over the cells until valid or unsolvable
            for i in range(0, index + 1):
                # Ignore the static cells
                if i in static_indexes:
                    continue
                # Reset the maxed out cells
                if board[i] == 9 and i != index:
                    board[i] = board_limit[i]
                # Incremenet the cell value
                else:
                    board[i] += 1
                    break

            # All cells being maxed out or static means it is unsolvable
            else:
                raise ValueError(f"no remaining updates for index {index}: board")

            # Capture the condition where it is unsolvable (all preceeding 9s)
            if all(
                [board[k] == 9 for k in range(index + 1) if k not in static_indexes]
            ):
                raise ValueError(f"no solution at index {index}: board")

            increments += 1

        # Print the update information and recurse forward
        print("Done %2d (%010d): %.4fs" % (index, increments, time.time() - start_time))
        return SudokuSolverV1.recursive_solve(index + 1, board, static_indexes)

    @classmethod
    def solve(cls, board: SudokuBoard) -> SudokuBoard:
        board = [int(i) for i in board.board]
        static_indexes = [i for i in range(81) if board[i] != 0]
        return SudokuSolverV1.recursive_solve(0, board, static_indexes)


# board = SudokuBoard(
#     "310450900072986143906010508639178020150090806004003700005731009701829350000645010"
# )

# out = SudokuSolverV1.solve(board)
# sol = (
#     "318457962572986143946312578639178425157294836284563791425731689761829354893645217"
# )
# print("".join([str(i) for i in out]) == sol)
