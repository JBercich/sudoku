#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import io
import re
import time
import logging
import argparse

logging.basicConfig(
    level=logging.DEBUG,
    datefmt="[%m-%d %H:%M:%S]",
    format="%(asctime)s %(name)-16s %(levelname)-9s %(message)s",
)

logger: logging.Logger = logging.getLogger("benchmarker")


class Timer:
    def __enter__(self) -> "Timer":
        self.start: float = time.time()
        return self

    def __exit__(self, *args) -> None:
        self.end: float = time.time()
        self.interval: float = self.end - self.start

    def get_time(self) -> float:
        return time.time() - self.start

    def __repr__(self) -> str:
        return f"{self.interval:>.6f}"

    def __str__(self) -> str:
        return f"{self.interval:>.6f}"


class PuzzleLoader:
    VALID_PUZZLE_SIZES: list[int] = [16, 81, 256, 625]

    @classmethod
    def load_puzzles(cls, nmax: int = -1) -> list[list[int]]:
        parser = argparse.ArgumentParser()
        parser.add_argument("filepath", type=argparse.FileType(), help="sudoku datafile")
        return cls.load_file(parser.parse_args().filepath, nmax)

    @classmethod
    def load_file(cls, file: io.TextIOWrapper, nmax: int = -1) -> list[list[int]]:
        # Prepare loading file contents reading all lines
        logger.info(f"Loading puzzles from file: {file.name}")
        file_lines: list[str] = file.readlines()
        logger.info(f"Loading {len(file_lines)} lines from file")
        nmax = nmax if nmax > 0 else len(file_lines)
        # Populate return list of integer problems
        puzzles: list[list[int]] = []
        for line_no, line in enumerate(file_lines):
            try:
                if (puzzle := cls.normalise_puzzle(line)) is not None:
                    puzzles.append(puzzle)
                else:
                    logger.info(f"Skipping contents on line {line_no + 1}")
            except ValueError as e:
                logger.warning(f"Skipping contents on line {line_no + 1} -> {e}")
            if len(puzzles) % 100000 == 0 and len(puzzles) != 0:
                logger.info(f"Loaded {len(puzzles):>9d} puzzles")
        logger.info(f"Loaded all {len(puzzles)} puzzles into memory")
        return puzzles

    @classmethod
    def normalise_puzzle(cls, puzzle: str) -> list[int] | None:
        if (puzzle := puzzle.strip()).startswith("#"):
            return None
        if len(puzzle := puzzle.strip()) not in cls.VALID_PUZZLE_SIZES:
            raise ValueError(f"Puzzle has invalid length: {len(puzzle)}")
        if not re.match(r"[\d|\.]*", puzzle):
            raise ValueError(f"Puzzle does not match regex: {puzzle}")
        return [int(x) if x != "." else 0 for x in puzzle]
