#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import math
from typing import Generator
from io import TextIOWrapper

import numpy as np


class DataLoader:
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
        return puzzle.strip()

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
            yield np.asarray([int(cell) for cell in puzzle], dtype=np.uint8)


if __name__ == "__main__":
    import sys
    import timeit

    target_file: str = "data/puzzles7" if len(sys.argv) == 1 else sys.argv[1]
    total_lines: int = np.sum([1 for _ in open(target_file).readlines()])

    def exhaust_native_loader(filepath: str = target_file):
        [_ for _ in DataLoader.load_file_to_native(open(filepath))]

    def exhaust_numpy_loader(filepath: str = target_file):
        [_ for _ in DataLoader.load_file_to_numpy(open(filepath))]

    print(f"  file: {target_file} has {total_lines} lines")
    t_native: list = timeit.repeat(number=1, repeat=10, stmt=exhaust_native_loader)
    print(f"native: {total_lines / np.mean(t_native):.6f} lines/sec")
    print(f"        {np.mean(t_native) / total_lines:.6f} secs/line")
    t_numpy: list = timeit.repeat(number=1, repeat=10, stmt=exhaust_numpy_loader)
    print(f" numpy: {total_lines / np.mean(t_numpy):.6f} lines/sec")
    print(f"        {np.mean(t_numpy) / total_lines:.6f} secs/line")
