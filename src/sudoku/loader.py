#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from typing import Generator
from io import TextIOWrapper
import math

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


def run_profile() -> None:
    """Container method for poetry scripting."""
    from argparse import ArgumentParser, FileType, Namespace
    import timeit

    parser: ArgumentParser = ArgumentParser(description="profile loaders")
    parser.add_argument("-f", required=True, type=FileType(), help="puzzle filepath")
    parser.add_argument("-o", default=False, type=bool, help="output csv profile")
    args: Namespace = parser.parse_args()

    repeats: int = 20
    num_lines: int = np.sum([1 for _ in open(args.f.name).readlines()])

    def exhaust_native_loader(parser: ArgumentParser = parser) -> None:
        [_ for _ in DataLoader.load_file_to_native(parser.parse_args().f)]

    def exhaust_numpy_loader(parser: ArgumentParser = parser) -> None:
        [_ for _ in DataLoader.load_file_to_numpy(parser.parse_args().f)]

    print(f"  file: {parser.parse_args().f.name} has {num_lines} lines")
    t_native: list = timeit.repeat(number=1, repeat=repeats, stmt=exhaust_native_loader)
    print(f"native: {num_lines / np.mean(t_native):.6f} lines/sec")
    print(f"        {np.mean(t_native) / num_lines:.6f} secs/line")
    t_numpy: list = timeit.repeat(number=1, repeat=repeats, stmt=exhaust_numpy_loader)
    print(f" numpy: {num_lines / np.mean(t_numpy):.6f} lines/sec")
    print(f"        {np.mean(t_numpy) / num_lines:.6f} secs/line")

    if args.o:
        with open("profile_loader.csv", "w") as fp:
            fp.write("native_loader,numpy_loader\n")
            for i in range(1, repeats):
                fp.write(f"{t_native[i] / num_lines:.9f},{t_numpy[i] / num_lines:.9f}\n")


if __name__ == "__main__":
    run_profile()
