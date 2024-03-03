#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import pytest

from sudoku.grid import (
    DEFAULT_CELL_MAXIMUM,
    DEFAULT_CELL_MINIMUM,
    DEFAULT_GRID_SIZE,
    Cell,
    Grid,
)


class TestGrid:
    def test_default_initialisation(self):
        """Grid initialisation with defaults creates an empty grid."""
        grid: Grid = Grid()
        assert grid._getter_counter == 0
        assert grid._grid_size == DEFAULT_GRID_SIZE
        assert grid.max_value == DEFAULT_CELL_MAXIMUM
        assert grid.min_value == DEFAULT_CELL_MINIMUM
        assert all([cell.is_empty() for cell in grid])

    def test_iter_dunder_method(self):
        """Iter dunder method holds logic for the grid field."""
        grid: Grid = Grid()
        for cell in grid:
            assert isinstance(cell, Cell)
            assert cell.is_empty()
            assert not cell.static
        assert len([i for i in grid]) == grid.get_grid_size() ** 2

    def test_getitem_dunder_method(self):
        """Get item dunder method holds logic for the grid field."""
        grid: Grid = Grid()
        assert isinstance(grid[0, 0], Cell)
        with pytest.raises(IndexError):
            _ = grid[grid.get_grid_size(), 0]
        with pytest.raises(TypeError):
            _ = grid[0]
        with pytest.raises(TypeError):
            _ = grid[0, 0, 0]

    def test_setitem_dunder_method(self):
        """Set item dunder method holds logic for the grid field."""
        grid: Grid = Grid()
        grid[0, 0] = grid.get_grid_size()
        assert grid[0, 0].value == grid.get_grid_size()
        with pytest.raises(IndexError):
            grid[grid.get_grid_size(), 0] = grid.get_grid_size()
        with pytest.raises(TypeError):
            grid[0] = grid.get_grid_size()
        with pytest.raises(TypeError):
            grid[0, 0, 0] = grid.get_grid_size()

    def test_get_grid_size(self):
        """Getting the grid size returns the provided default or parameter value."""
        grid: Grid = Grid(size=4)
        assert grid.get_grid_size() == 4

    def test_get_subgrid_size(self):
        """Getting the subgrid size returns the provided default or parameter value."""
        grid: Grid = Grid(size=4)
        assert grid.get_subgrid_size() == 2

    def test_get_row(self):
        """Getting a grid row returns the expected size and values."""
        grid: Grid = Grid(size=4)
        assert len(grid.get_row(0)) == grid.get_grid_size()

    def test_get_column(self):
        """Getting a grid column returns the expected size and values."""
        grid: Grid = Grid(size=4)
        assert len(grid.get_column(0)) == grid.get_grid_size()

    def test_get_subgrid(self):
        """Getting a grid subgrid returns the expected size and values."""
        grid: Grid = Grid(size=4)
        assert len(grid.get_subgrid(0, 0)) == grid.get_grid_size()

    def test_valid_init_empty_grid(self):
        """Initialising an empty grid with a valid size creates correct grid cells."""
        grid: Grid = Grid._init_empty_grid(size=4)
        assert all([cell.is_empty() for row in grid for cell in row])

    def test_validate(self):
        """Grid validation should capture incomplete or constrain breaching grids."""
        grid: Grid = Grid()
        assert grid.validate()
        grid[0, 0] = 1
        assert grid.validate()
        grid[0, 1] = 1
        assert not grid.validate()
        grid[0, 1] = grid[1, 0].value
        grid[1, 0] = 1
        assert not grid.validate()
        grid[1, 0] = grid[1, 1].value
        grid[1, 1] = 1
        assert not grid.validate()

    def test_load_string(self):
        """Loading a string should set values correctly and set them as static."""
        grid_string: str = "0" * 4
        grid: Grid = Grid.load_string(grid_string)
        assert all([cell.is_empty() for cell in grid])
        assert len([cell for cell in grid]) == grid.get_grid_size() ** 2

    def test_dump_string(self):
        """Dumping a string should have the correct length and values."""
        grid: Grid = Grid(size=4)
        assert grid.dump_string() == "0" * 4**2
