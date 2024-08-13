#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import math
from typing import Generator
from io import TextIOWrapper

import numpy as np


class DataLoader:
    _CELL_ENCODING: tuple[str, str] = (".", "0")
    _LINE_SKIP_CHR: tuple[str, ...] = ("#",)

    @classmethod
    def check_puzzle_skip_chr(cls, puzzle: str) -> bool:
        """Check puzzle can be skipped with skip character."""
        puzzle_dimension: float = math.sqrt(len(puzzle))
        return puzzle_dimension == int(puzzle_dimension)

    @classmethod
    def check_puzzle_length(cls, puzzle: str) -> bool:
        """Check puzzle is square for given string length."""
        puzzle_dimension: float = math.sqrt(len(puzzle))
        return puzzle_dimension == int(puzzle_dimension)

    @classmethod
    def serialize_puzzle(cls, puzzle: str) -> str:
        """Coerce puzzle string into required format."""
        return puzzle.strip().replace(*cls._CELL_ENCODING)

    @classmethod
    def load_file_to_native(cls, fp: TextIOWrapper) -> Generator[list[int], None, None]:
        """Generate native puzzle data structures from a file."""
        for puzzle_line in fp:
            puzzle: str = cls.serialize_puzzle(puzzle_line)
            if not cls.check_puzzle_length(puzzle):
                raise ValueError(f"Puzzle has invalid length: {len(puzzle)}")
            yield [int(cell) for cell in puzzle]

    @classmethod
    def load_file_to_numpy(cls, fp: TextIOWrapper) -> Generator[np.ndarray, None, None]:
        """Generate numpy puzzle data structures from a file."""
        for puzzle_line in fp:
            puzzle: str = cls.serialize_puzzle(puzzle_line)
            if not cls.check_puzzle_length(puzzle):
                raise ValueError(f"Puzzle has invalid length: {len(puzzle)}")
            yield np.ndarray([int(cell) for cell in puzzle], dtype=np.uint8)


loader = DataLoader.load_file_to_native(open("./data/puzzles0_kaggle"))
for i in range(10):
    print(loader.__next__())
