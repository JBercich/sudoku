#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from typer import Typer, Option, Context, Exit
from rich.console import Console

from sudoku_cli import __version__

app: Typer = Typer(
    invoke_without_command=True,
    pretty_exceptions_show_locals=False,
)
console: Console = Console()


def display_version(ctx: Context, display_version_flag: bool):
    if display_version_flag:
        console.print(f"{ctx.info_name} {__version__}")
        raise Exit()


@app.callback()
def callback(
    ctx: Context,
    _: bool = Option(False, "--version", callback=display_version),
) -> None:
    if ctx.invoked_subcommand is None:
        console.print(ctx.get_help())
