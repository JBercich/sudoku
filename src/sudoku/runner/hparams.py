#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""Sudoku solver hyperparameter grid."""

from itertools import product


class HyperparameterGrid:
    """Hyperparameter grid constructor."""

    @staticmethod
    def __new__(self, **kwargs) -> dict:
        # Check all hyperparameter options are given as lists
        for k, v in kwargs.items():
            if not isinstance(v, list):
                raise ValueError(f"Hyperparameter grid requires list of options: {k}")
        # Create cartesian product of hyperparameters
        return [
            {parameter: value for parameter, value in zip(kwargs.keys(), parameter_set)}
            for parameter_set in [
                parameter_subset for parameter_subset in product(*kwargs.values())
            ]
        ]
