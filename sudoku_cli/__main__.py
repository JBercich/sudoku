#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import time
from enum import Enum, unique
from typing import Annotated, TypeAlias

from typer import Typer, Option, Context, Exit, FileText
from rich.console import Console
from rich.progress import track

from sudoku_cli import __version__
from sudoku_cli.sudoku import Grid
from sudoku_cli.sudoku.solvers import ExactCover

app: Typer = Typer(
    name="sudoku-cli",
    invoke_without_command=True,
    pretty_exceptions_show_locals=False,
)
console: Console = Console()


# ::MARK:: Option callbacks
# Callback methods are defined for specifc command arguments or options
# per typer application. Usually used for options, callbacks check non-
# null values and can either exit or return a specific result.


def version(ctx: Context, display_version_flag: bool) -> None:
    if display_version_flag:
        console.print(f"{ctx.info_name} {__version__}")
        raise Exit()


def parse_grid_file(ctx: Context, sudoku_file: FileText) -> list[Grid]:
    if sudoku_file is not None:
        return [Grid(row.strip()) for row in sudoku_file]
    return []


def parse_grid_args(ctx: Context, sudoku_args: list[str]) -> list[Grid]:
    if sudoku_args is not None:
        return [Grid(grid) for grid in sudoku_args]
    return []


# ::MARK:: Shared parameters
# Certain arguments and options are shared between different commands
# in the top-level application such as how sudoku grids are provided
# and these shared definitions and callbacks.


SudokuArgs: TypeAlias = Annotated[
    list[str],
    Option(
        "--grid",
        "-g",
        show_default=False,
        callback=parse_grid_args,
        help="Sudoku grid string arrays.",
    ),
]
SudokuFile: TypeAlias = Annotated[
    FileText,
    Option(
        "--file",
        "-f",
        show_default=False,
        callback=parse_grid_file,
        help="Line-delimited grid string array file.",
    ),
]


@unique
class SolverOption(str, Enum):
    BACKTRACKING = "backtracking"


GridSolver: TypeAlias = Annotated[
    SolverOption,
    Option(
        "--solver",
        "-s",
        help="Solver algorithm used for each sudoku grid.",
    ),
]

# ::MARK:: App commands
# Application commands encompass under a solve() method to test various
# solver algorithms and output solved grids (if possible) and otherwise
# profile() the algorithm parameters.


@app.callback(no_args_is_help=True)
def callback(_: bool = Option(False, "--version", callback=version)) -> None:
    """
    CLI for solving and profiling different sudoku algorithms.
    """


@app.command(no_args_is_help=True)
def solve(
    grid_args: SudokuArgs = None,
    grid_file: SudokuFile = None,
    solver: GridSolver = SolverOption.BACKTRACKING,
) -> None:
    """
    Solve a sudoku grid for a file or list of grids using a solver.
    """
    grids: list[Grid] = grid_args if grid_args is not None else []  # type: ignore
    grids += grid_file if grid_file is not None else []
    for i, grid in track(enumerate(grids, 1), description="Solving"):
        t0 = time.time()
        ExactCover.solve(grid)
        # print(grid.values)
        print(time.time() - t0)
        if grid.is_complete():
            print("Solved")
        # break
        if i > 10:
            break


@app.command(no_args_is_help=True)
def profile(
    grid_args: SudokuArgs = None,
    grid_file: SudokuFile = None,
    solver: GridSolver = SolverOption.BACKTRACKING,
) -> None:
    """
    Profile a sudoku solver algorithm against a collection of grids.
    """
    grids: list[Grid] = grid_args if grid_args is not None else []  # type: ignore
    grids += grid_file if grid_file is not None else []
    for grid in track(grids, description="Profiling"):
        pass


if __name__ == "__main__":
    app()
