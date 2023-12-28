#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import pytest

from sudoku.cell import Cell
from sudoku.grid import Grid


@pytest.mark.skip("Refactoring")
class TestGrid:
    def test_grid_is_valid(self):
        """Default grid initialises correctly with defaults."""

        # Validate starting count and cell values
        grid: Grid = Grid()
        assert grid._get_count == 0
        for row in grid.grid:
            for col in row:
                assert col.value == 0

    def test_grid_getter_increments(self):
        """Grid access should increment the global grid access counter."""

        # Initialise and validate base grid
        grid: Grid = Grid()
        assert grid._get_count == 0

        # Increment the grid counter
        _ = grid.grid
        assert grid._get_count == 1

    def test_setitem_index_raises(self):
        """Invalid index access of the grid raises TypeError."""

        # Invalid grid access without a collection-based (row, col) access
        with pytest.raises(TypeError):
            Grid()[0]
        with pytest.raises(TypeError):
            Grid()["Invalid Access Key"]
        with pytest.raises(TypeError):
            Grid()[0, 1, 2]
        with pytest.raises(IndexError):
            Grid()[10, 0]
        with pytest.raises(IndexError):
            Grid()[0, 10]

    def test_getitem_index_raises(self):
        """Invalid index access of the grid raises TypeError."""

        # Invalid grid access without a collection-based (row, col) access
        with pytest.raises(TypeError):
            Grid()[0] = 0
        with pytest.raises(TypeError):
            Grid()["Invalid Access Key"] = 0
        with pytest.raises(TypeError):
            Grid()[0, 1, 2] = 0
        with pytest.raises(IndexError):
            Grid()[10, 0] = 0
        with pytest.raises(IndexError):
            Grid()[0, 10] = 0

    def test_getitem_index_yield_cell(self):
        """Valid grid index getting will retrieve the cell instance."""

        # Initialise and access a grid cell
        grid: Grid = Grid()
        assert isinstance(grid[0, 0], Cell)
        assert grid[0, 0].value == 0

    def test_setitem_index_yield_cell(self):
        """Valid grid index access yield a cell instance with a value."""

        # Initialise and set a grid cell and validate an update
        grid: Grid = Grid()
        assert grid[0, 0].value == 0
        grid[0, 0] = 1
        assert grid[0, 0].value == 1
        assert grid[0, 0]._set_count == 1

    def test_validate_row_constraint(self):
        """Grids validated with invalid rows return False."""

        # Construct an invalid grid
        grid: Grid = Grid()
        grid[0, 0] = 1
        assert grid.validate()
        grid[0, 1] = 1
        assert not grid.validate()

    def test_validate_col_constraint(self):
        """Grids validated with invalid columns return False."""

        # Construct an invalid grid
        grid: Grid = Grid()
        grid[0, 0] = 1
        assert grid.validate()
        grid[1, 0] = 1
        assert not grid.validate()

    def test_validate_grid_constraint(self):
        """Grids validated with invalid smaller grids return False."""

        # Construct an invalid grid
        grid: Grid = Grid()
        grid[0, 0] = 1
        assert grid.validate()
        grid[1, 1] = 1
        assert not grid.validate()

    def test_validate(self):
        """Grids validated without breaching constraints return True."""

        # Construct a valid grid
        grid: Grid = Grid()
        assert grid.validate()

    def test_load_invalid_string(self):
        """Loading an invalid string raises ValueError."""

        # Create and attempt to load an invalid grid
        invalid_grid: str = "1" * Grid.COLS * Grid.ROWS
        invalid_grid_message: str = rf"Loaded sudoku board is not valid: {invalid_grid}"
        with pytest.raises(ValueError, match=invalid_grid_message):
            Grid.load_string(invalid_grid)

    def test_load_valid_string(self):
        """Valid sudoku board strings are loaded, with all 0 counter cells."""

        # Create a valid grid and check cell counters
        valid_grid: str = "0" * Grid.COLS * Grid.ROWS
        grid: Grid = Grid.load_string(valid_grid)
        for row in grid.grid:
            for col in row:
                assert col._get_count == 0
                assert col._set_count == 0
        assert grid.validate()
