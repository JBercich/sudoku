#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from abc import ABC


class SudokuException(Exception, ABC):
    pass


class GridException(SudokuException):
    pass
