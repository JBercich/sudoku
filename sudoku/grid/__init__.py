#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
Sudoku Grid
-----------
Python native implementation for sudoku grids and relevant operations
applying to grid validation or internal grid manipulation. Grid sizes
are constrained with a `Grid.MAX_DIM` as a $5 \\times 5$ problem since
this restricts list sizes to a manageable 625 array length. Longer grid
sizes could allow for different implementations such as using NumPy as
the backbone for sudoku operations.

Basic operations leverage simple slices in memory or basic numerical
comparisons meaning that the added NumPy overhead can impact the time
of certain processes on the grid.
"""

from sudoku.grid.grid import Grid
from sudoku.grid.validate import Validator

__all__ = ["Grid", "Validator"]
