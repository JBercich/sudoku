#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import csv
from collections import defaultdict

from sudoku.sudoku import Sudoku
from sudoku.solver import BackTrackingSolver, Solver
from benchmark_utils import Timer, PuzzleLoader, logger  # type: ignore # noqa: F401


if __name__ == "__main__":
    with Timer() as read_timer:
        puzzles: list[list[int]] = PuzzleLoader.load_puzzles()
    logger.info(f"Time for loading all puzzles: {read_timer}s")

    with Timer() as loop_timer:
        res: dict[str, list[float]] = defaultdict(list)
        for i, puzzle in enumerate(puzzles, 1):
            with Timer() as total_timer:
                cells: str = "".join([str(x) for x in puzzle])
                solver: Solver = BackTrackingSolver(Sudoku(cells=cells))
                with Timer() as setup_timer:
                    solver.setup()
                with Timer() as solve_timer:
                    solver.solve()
                with Timer() as check_timer:
                    solved: bool = solver.check()
                    if not solved:
                        print("Failed")
            res["PuzzleId"].append(i)
            res["IsSolved"].append(solved)
            res["TotalTime"].append(total_timer.interval)
            res["SetupTime"].append(setup_timer.interval)
            res["SolveTime"].append(solve_timer.interval)
            res["CheckTime"].append(check_timer.interval)
            if i % 100 == 0 and i != 0:
                logger.info(f"Solved {i:>9d} puzzles")
                logger.info(f"Intermediate result: {i/loop_timer.get_time()} puzzles/s")
    logger.info(f"Time for solving all puzzles: {loop_timer}s")
    logger.info(f"Final profile result: {len(puzzles)/loop_timer.interval} puzzles/s")
    with open("benchmark_backtracking.csv", "w") as fp:
        writer = csv.writer(fp)
        writer.writerow(res.keys())
        writer.writerows(zip(*res.values()))

# import time
# from pathlib import Path
# from collections import defaultdict

# import pandas as pd

# from sudoku.sudoku import Sudoku
# from sudoku.solver import Solver, BackTrackingSolver


# class Timer:
#     def __enter__(self):
#         self.start = time.clock()
#         return self

#     def __exit__(self, *args):
#         self.end = time.clock()
#         self.interval = self.end - self.start


# def load_sudokus(filepath: Path, num: int = 250) -> list:
#     pbms: list = []
#     with open(filepath, "r") as fp:
#         for _ in range(num):
#             pbm: str = fp.readline().strip()
#             pbms.append(fp.readline().strip().split(",")[:2] if "," in pbm else pbm)
#     return pbms


# def solve_problems(sudokus: list, solver_cls: type) -> pd.DataFrame:
#     res: dict[str, list] = defaultdict(list)
#     for i, (cells, _) in enumerate(sudokus, 1):
#         res["sudoku_id"].append(i)
#         t_total: float = time.time()
#         sudoku: Sudoku = Sudoku(cells=cells)
#         solver: Solver = solver_cls(sudoku)
#         t_setup: float = time.time()
#         solver.setup()
#         res["setup_time"].append(time.time() - t_setup)
#         t_solve: float = time.time()
#         solver.solve()
#         res["solve_time"].append(time.time() - t_solve)
#         t_check: float = time.time()
#         res["is_solved"].append(sudoku.is_complete())
#         res["check_time"].append(time.time() - t_check)
#         res["total_time"].append(time.time() - t_total)
#         print(f"Solved ({res['is_solved'][-1]}): {res['total_time'][-1]:.4f}s")
#     return pd.DataFrame(res)


# results: pd.DataFrame = solve_problems(
#     load_sudokus(temp_filepath, num=100),
#     BackTrackingSolver,
# )
# print(results.describe())
