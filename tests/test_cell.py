#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from typing import Any

import pytest

from sudoku.cell import Cell


class TestCell:
    def test_cell_is_valid(self):
        """Default cell dataclass assignment correctly initialises and instance."""

        # Cell instantiation and default value setting should be expected
        cell: Cell = Cell(value=0)
        assert cell is not None
        assert cell._get_count == 0
        assert cell._set_count == 0
        assert cell.value == 0

    @pytest.mark.parametrize("value", [-1, -0.5, -0.1, 9.1, 9.5, 10])
    def test_cell_value_is_out_of_range(self, value: Any):
        """Cell with value values outside of valid range raises."""

        # Invalid cell values are outside the range 0-9 (integer)
        with pytest.raises(ValueError, match=rf"Invalid cell value: {value}"):
            Cell(value=value)

    def test_cell_value_setter_counter_increments(self):
        """Cell value setter increments internal counter attribute."""

        # Build a cell and show how setter functions impact the counter
        cell: Cell = Cell(value=0)
        assert cell._set_count == 0
        cell.value = 0
        assert cell._set_count == 1

    def test_cell_value_getter_counter_increments(self):
        """Cell value getter increments internal counter attribute."""

        # Build a cell and show how getter functions impact the counter
        cell: Cell = Cell(value=0)
        assert cell._get_count == 0
        _ = cell.value
        assert cell._get_count == 1

    def test_eq_dunder_method(self):
        """Cell equality is performed between cell values."""

        # Construct cell instances
        base_cell: Cell = Cell(value=0)
        same_cell: Cell = Cell(value=0)
        diff_cell: Cell = Cell(value=1)

        # Compare the cell instances
        assert base_cell == same_cell
        assert base_cell != diff_cell

    def test_lt_dunder_method(self):
        """Cell less than comparison is performed between cell values."""

        # Construct cell instances
        base_cell: Cell = Cell(value=0)
        same_cell: Cell = Cell(value=0)
        diff_cell: Cell = Cell(value=1)

        # Compare the cell instances
        assert (base_cell < same_cell) == False
        assert (base_cell < diff_cell) == True

    def test_reset_counters(self):
        """Resetting the cell counters should revert the values to 0."""

        # Create a cell with non-zero counters
        cell: Cell = Cell(value=0)
        cell.value = 1
        _ = cell.value
        assert cell._get_count != 0
        assert cell._set_count != 0

        # Reset the counters and verify they are set to 0
        cell.reset_counters()
        assert cell._get_count == 0
        assert cell._set_count == 0
