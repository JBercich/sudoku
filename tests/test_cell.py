#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import pytest

from sudoku.grid import (
    DEFAULT_CELL_MAXIMUM,
    DEFAULT_CELL_MINIMUM,
    EMPTY_CELL_VALUE,
    Cell,
)


class TestCell:
    def test_default_initialisation(self):
        """Default initialisation correctly sets default values."""
        cell: Cell = Cell()
        assert cell is not None
        assert cell._getter_counter == 0
        assert cell._setter_counter == 0
        assert cell.value == EMPTY_CELL_VALUE
        assert not cell.static
        assert cell.minimum_value == DEFAULT_CELL_MINIMUM
        assert cell.maximum_value == DEFAULT_CELL_MAXIMUM

    def test_value_default_empty_for_property(self):
        """Initialisation with a property field value defaults to an empty cell."""
        assert Cell().value == EMPTY_CELL_VALUE

    @pytest.mark.parametrize("value", [EMPTY_CELL_VALUE - 1, DEFAULT_CELL_MAXIMUM + 1])
    def test_value_outside_range_raises(self, value: int):
        """Setting a value with an out-of-range value raises a ValueError."""
        with pytest.raises(ValueError, match=rf"Invalid cell value: {value}"):
            Cell(value=value)

    def test_value_static_cell_raises(self):
        """Setting a value for a static cell raises a RuntimeError."""
        cell: Cell = Cell(static=True)
        with pytest.raises(RuntimeError, match=r"Cannot modify a static cell."):
            cell.set_empty_value()

    def test_value_getter_increments_counter(self):
        """Getting a value field increments the getter counter by 1."""
        cell: Cell = Cell()
        assert cell._getter_counter == 0
        _ = cell.value
        assert cell._getter_counter == 1

    def test_value_setter_increments_counter(self):
        """Setting a value field increments the setter counter by 1."""
        cell: Cell = Cell()
        assert cell._setter_counter == 0
        cell.set_empty_value()
        assert cell._setter_counter == 1

    def test_minimum_value_frozen(self, filter_cell_warnings):
        """Cell minimum_value field is unchanged with the setter."""
        cell: Cell = Cell()
        assert cell.minimum_value == DEFAULT_CELL_MINIMUM
        cell.minimum_value += 1
        assert cell.minimum_value == DEFAULT_CELL_MINIMUM

    def test_eq_dunder_method(self):
        """Equality dunder method holds logic for the value field."""
        assert Cell() == Cell()
        assert Cell().value == Cell().value
        assert Cell() == Cell(static=True)
        assert Cell().value == Cell(static=True).value

    def test_lt_dunder_method(self):
        """Less than dunder method holds logic for the value field."""
        assert Cell() < Cell(value=DEFAULT_CELL_MAXIMUM)
        assert Cell().value < Cell(value=DEFAULT_CELL_MAXIMUM).value
        assert Cell() < Cell(value=DEFAULT_CELL_MAXIMUM, static=True)
        assert Cell().value < Cell(value=DEFAULT_CELL_MAXIMUM, static=True).value

    def test_set_empty_field(self):
        """The empty field setter should set the value as an empty value."""
        cell: Cell = Cell(value=DEFAULT_CELL_MAXIMUM)
        assert cell.value == DEFAULT_CELL_MAXIMUM
        assert cell.value != EMPTY_CELL_VALUE
        cell.set_empty_value()
        assert cell.value == EMPTY_CELL_VALUE

    def test_is_empty(self):
        """The is empty checker should correctly indicate an empty cell value."""
        cell: Cell = Cell()
        assert cell.value == EMPTY_CELL_VALUE
        assert cell.is_empty()
        cell.value = DEFAULT_CELL_MAXIMUM
        assert cell.value != EMPTY_CELL_VALUE
        assert not cell.is_empty()

    @pytest.mark.parametrize(
        "value",
        [
            EMPTY_CELL_VALUE,
            DEFAULT_CELL_MINIMUM,
            DEFAULT_CELL_MAXIMUM,
            DEFAULT_CELL_MINIMUM + 1,
            DEFAULT_CELL_MAXIMUM - 1,
        ],
    )
    def test_value_is_valid(self, value: int):
        """Value is valid correctly verifies an integer is in the correct range."""
        assert Cell().value_is_valid(value)

    @pytest.mark.parametrize(
        "value",
        [
            EMPTY_CELL_VALUE - 1,
            -1 * DEFAULT_CELL_MINIMUM,
            -1 * DEFAULT_CELL_MAXIMUM,
            DEFAULT_CELL_MAXIMUM + 1,
        ],
    )
    def test_value_is_not_valid(self, value: int):
        """Value is valid correctly verifies an integer is not in the correct range."""
        assert not Cell().value_is_valid(value)

    def test_reset_getter_counter(self):
        """Resetting the getter counter correctly resets to 0."""
        cell: Cell = Cell()
        cell.value
        assert cell._getter_counter != 0
        cell.reset_getter_counter()
        assert cell._getter_counter == 0

    def test_reset_setter_counter(self):
        """Resetting the setter counter correctly resets to 0."""
        cell: Cell = Cell()
        cell.set_empty_value()
        assert cell._setter_counter != 0
        cell.reset_setter_counter()
        assert cell._setter_counter == 0

    def test_reset_counters(self):
        """Resetting counters correctly resets both getter nd setter counts to 0."""
        cell: Cell = Cell()
        cell.value, cell.set_empty_value()
        assert cell._getter_counter != 0
        assert cell._setter_counter != 0
        cell.reset_counters()
        assert cell._getter_counter == 0
        assert cell._setter_counter == 0
