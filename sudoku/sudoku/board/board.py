#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import re
from typing import Any, final
from abc import ABC, abstractmethod, abstractproperty


class SudokuBoard(ABC):
    """
    Sudoku board.

    A sudoku board can be solved by a solver. The default and most portable format for
    the boards is a single string of cells from left-right and top-down. A 0 encodes the
    empty cell for an incomplete board.
    """

    @abstractproperty
    def NAME(self) -> str:
        pass

    @abstractproperty
    def DESC(self) -> str:
        pass

    @final
    def __init__(self, board: str) -> None:
        self.board: str = self.setup(self.validate(board))

    @final
    def __repr__(self) -> str:
        """
        Class string representation.

        Return the given board information such as the name and description.

        Returns:
            str: Class string representation of board metadata.
        """
        repr_string: str = "{}: {}".format(self.NAME, self.DESC)
        return repr_string

    @final
    def __str__(self) -> str:
        """
        String board representation.

        Return a board as a string using box unicode characters for easy visualisation.
        Empty cells denoted by 0s are left empty and grid lines are shown to be thick on
        the larger grid outlines and thin grid for inner-grid lines.

        Returns:
            str: Unicode string representation of the board.
        """
        # Convert board cell entries to string characters, replace 0 with a space
        board: list[str] = [str(v) if str(v) != "0" else " " for v in self.board]

        # Define board grid partitions
        col_line: str = "    1   2   3   4   5   6   7   8   9  \n"
        top_line: str = "  ┏━━━┯━━━┯━━━┳━━━┯━━━┯━━━┳━━━┯━━━┯━━━┓\n"
        mid_line: str = "  ┠───┼───┼───╂───┼───┼───╂───┼───┼───┨\n"
        sep_line: str = "  ┣━━━┿━━━┿━━━╋━━━┿━━━┿━━━╋━━━┿━━━┿━━━┫\n"
        bot_line: str = "  ┗━━━┷━━━┷━━━┻━━━┷━━━┷━━━┻━━━┷━━━┷━━━┛\n"

        # Define helper lambda function of single grid rows
        def draw_row(row_number: int, row_values: list[str]) -> str:
            row_format: str = " {} ┃ {} │ {} │ {} ┃ {} │ {} │ {} ┃ {} │ {} │ {} ┃\n"
            return row_format.format(row_number, *row_values)

        # Draw sudoku board by each row
        board_string: str = col_line + top_line
        for row_number in range(1, 10):
            # Skip drawing a grid for the first row
            if row_number != 1:
                # Each separator line differs depending on the row number
                board_string += sep_line if row_number % 3 == 1 else mid_line
            # Draw the row with the correctly indexed values
            bot_index: int = (row_number - 1) * 9
            top_index: int = row_number * 9
            board_string += draw_row(row_number, board[bot_index:top_index])
        # Append the final bottom line of the board
        board_string += bot_line
        return board_string

    def __getitem__(self, selection: Any) -> Any:
        """
        Get item from the board using some selection.

        Args:
            selection (Any): Generic indexing integer, slice or key.

        Returns:
            Any: Resulting slice or value from the board for the given selection.
        """
        return self.board[selection]

    def __setitem__(self, selection: Any, value: Any) -> None:
        """
        Set an item in the board for the given selection.

        Args:
            selection (Any): Generic indexing integer, slice or key.
            value (Any): Value used to set the board selection.

        Raises:
            ValueError: Value is not an integer type.
            ValueError: Value is not in the correct integer range.
        """
        # Setting values required to be an integer
        if not isinstance(value, int):
            raise ValueError(f"value can only be set using {int}: {value}")

        # Setting values required to be in the range 0-9
        if value < 0 or value > 9:
            raise ValueError(f"value to set board outside of range [0,9]: {value}")

        self.board[selection] = value

    @final
    def validate(self, board: str) -> str:
        """
        Validate the input string-format board.

        For the default input format of a string board, validation of the input is done
        to confirm whether the board is valid from an initial level. Only constraints
        are checked such as column, row and grid restrictions.

        Args:
            board (str): Input board string to validate.

        Returns:
            str: Input board string unchanged.

        Raises:
            ValueError: Board string is incorrectly typed.
            ValueError: Board string does not match the regex of 81 integers [0-9].
            ValueError: Board does not uphold a row, column or grid constraint.
        """
        try:
            # Verify board matches required regex pattern
            assert re.fullmatch(r"[0-9].{80}", board) is not None

            # Verify board upholds constraints in all columns, rows and grids
            for index in range(9):
                # Get lists of each of the constrained sudoku board fields
                row: list = [board[index + p] for p in range(0, 9)]
                column: list = [board[index + p] for p in range(0, 81, 9)]
                grid: list = [
                    board[(index * 3) + (row_index * 9) + col_index]
                    for row_index in range(3)
                    for col_index in range(3)
                ]
                # Check each field contains at most 1 of every value
                for value in range(1, 10):
                    if row.count(value) > 1:
                        raise ValueError(f"[{index},{value}] Invalid row: {row}")
                    if column.count(value) > 1:
                        raise ValueError(f"[{index},{value}] Invalid column: {column}")
                    if grid.count(value) > 1:
                        raise ValueError(f"[{index},{value}] Invalid grid: {grid}")

        except TypeError:
            # Input board is expected to be typed as a string
            raise ValueError(f"board must be {str}, not {type(board)}")

        except AssertionError:
            # Expected input board regex to consistent of 81 characters [0-9]
            raise ValueError(f"board must have 81 cells with digits 0-9: {board}")

        finally:
            return board

    @abstractmethod
    def setup(self, board: str) -> Any:
        """
        Setup the board into the given data structure. If necessary, additionally adding
        overriding methods for `__getitem__` and `__setitem__` should be done also.

        Args:
            board (str): Input string board representation.

        Returns:
            Any: Board contained within a different data structure.
        """
        pass

    @abstractmethod
    def to_string(self) -> str:
        """
        Reversal method of the `setup()` function which converts the board instance that
        has been setup back into the default input string representation.

        Returns:
            str: Input string board representation.
        """
        pass
