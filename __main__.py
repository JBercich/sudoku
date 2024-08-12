#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import time
from pathlib import Path
from collections import defaultdict

import pandas as pd

from sudoku.sudoku import Sudoku
from sudoku.solver import Solver, BackTrackingSolver

temp_filepath: Path = Path().resolve() / "data" / "sudoku.csv"


class Timer:
    def __enter__(self):
        self.start = time.clock()
        return self

    def __exit__(self, *args):
        self.end = time.clock()
        self.interval = self.end - self.start


def load_sudokus(filepath: Path, num: int = 250) -> list:
    pbms: list = []
    with open(filepath, "r") as fp:
        for _ in range(num):
            pbm: str = fp.readline().strip()
            pbms.append(fp.readline().strip().split(",")[:2] if "," in pbm else pbm)
    return pbms


def solve_problems(sudokus: list, solver_cls: type) -> pd.DataFrame:
    res: dict[str, list] = defaultdict(list)
    for i, (cells, _) in enumerate(sudokus, 1):
        res["sudoku_id"].append(i)
        t_total: float = time.time()
        sudoku: Sudoku = Sudoku(cells=cells)
        solver: Solver = solver_cls(sudoku)
        t_setup: float = time.time()
        solver.setup()
        res["setup_time"].append(time.time() - t_setup)
        t_solve: float = time.time()
        solver.solve()
        res["solve_time"].append(time.time() - t_solve)
        t_check: float = time.time()
        res["is_solved"].append(sudoku.is_complete())
        res["check_time"].append(time.time() - t_check)
        res["total_time"].append(time.time() - t_total)
        print(f"Solved ({res['is_solved'][-1]}): {res['total_time'][-1]:.4f}s")
    return pd.DataFrame(res)


results: pd.DataFrame = solve_problems(
    load_sudokus(temp_filepath, num=100),
    BackTrackingSolver,
)
print(results.describe())
