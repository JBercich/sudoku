#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from abc import ABC, abstractmethod


class Solver(ABC):
    name: str

    @classmethod
    @abstractmethod
    def solve(cls, *args, **kwargs):
        pass
